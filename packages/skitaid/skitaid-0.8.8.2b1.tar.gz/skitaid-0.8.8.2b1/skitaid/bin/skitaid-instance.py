#!/usr/bin/python3
# 2014. 12. 9 by Hans Roh hansroh@gmail.com

import sys, os, getopt
from skitai.server import Skitai
from skitai.server.rpc.cluster_manager import AccessPolicy
from skitai import lifetime
from aquests.lib import confparse, flock, pathtool
import skitai
import skitaid
import signal
try:
	import hotshot
except ImportError:
	import profile as hotshot

skitai.NAME = "SWAED/%s.%s (Skitai %s.%s)" % (skitaid.version_info [:2] + skitai.version_info [:2])

def traceback ():
	t, v, tb = sys.exc_info()
	tbinfo = []
	assert tb # Must have a traceback
	while tb:
		tbinfo.append((
			tb.tb_frame.f_code.co_filename,
			tb.tb_frame.f_code.co_name,
			str(tb.tb_lineno)
			))
		tb = tb.tb_next

	del tb
	file, function, line = tbinfo [-1]
	buf = []
	buf.append ("%s %s" % (t, v))
	buf.append ("in file %s at line %s, %s" % (file, line, function == "?" and "__main__" or "function " + function))
	buf += ["%s %s %s" % x for x in tbinfo]
	return "\n".join (buf)


		
class	WAS (Skitai.Loader):
	def __init__ (self, config, logpath, varpath, consol):
		self.test_config (config)
		self.consol = consol
		self.ssl_server = False
		Skitai.Loader.__init__ (self, config, logpath, varpath)
	
	@classmethod
	def test_config (cls, conf):
		config = confparse.ConfParse (conf)
		
		assert config.getint ("server", "processes", 1) > 0, "processes should be int >= 1"
		assert config.getint ("server", "threads", 4) >= 0, "processes should be int >= 0"
		if config.getopt ("ssl", "enable_ssl") == "yes":
			assert config.getopt ("ssl", "certfile"), "enable ssl but certfile is not given"
			assert config.getopt ("ssl", "passphrase"), "enable ssl but pass_phrase is not given"
		assert config.getint ("server", "port", 5000) > 0, "posrt should br int > 0"		
		assert config.getint ("tunefactors", "static_max_age", 300) >= 0, "static_max_age should be int >= 0"
		assert config.getint ("tunefactors", "keep_alive", 10) >= 0, "keep_alive should be int >= 0"
		assert config.getint ("tunefactors", "response_timeout", 10) >= 0, "response_timeout should be int >= 0"
		assert config.getint ("tunefactors", "num_result_cache_max", 1000) >= 0, "num_result_cache_max should be int >= 0"
		
		for sect in list(config.keys ()):
			if sect.startswith ("@"):
				name = sect [1:]
				ctype = config.getopt (sect, "type")
				if ctype == "postgresql":
					try:
						import psycopg2
					except ImportError:
						raise AssertionError ("psycopg2 not installed")
				assert len (name) > 0, "cluster name should be provided"
				members = [_f for _f in [x.strip () for x in config.getopt (sect, "members").split (",")] if _f]
				assert len (members) > 0, "cluster should have al least one member"				
				
	def to_list (self, text, delim = ","):
		return [_f for _f in [x.strip () for x in text.split (",")] if _f]	
			
	def configure (self):
		global _profile
		
		if self.consol:
			self.wasc.logger.add_screen_logger ()
		
		# before spawn
		config = confparse.ConfParse (self.config)
		self.wasc.register ("config", config)
		
		if _profile:
			self.wasc.logger ("server", "perf profiling is turned on, set to single worker mode forcely", "warn")
			self.set_num_worker (1)
		else:	
			self.set_num_worker (config.getint ("server", "processes", 1))
		
		if config.getint ("server", "threads", 4) == 0:
			self.wasc.logger ("server", "multi-threading is disabled, all asynchronous remote call services will be also disabled.", "warn")
			
		if config.getopt ("ssl", "enable_ssl") in ("yes", "1") and config.getopt ("ssl", "certfile"):
			certfile, keyfile = config.getopt ("ssl", "certfile", None), config.getopt ("ssl", "keyfile", None)
			if not os.path.isfile (certfile):
				_certpath = os.path.join (os.path.split (os.path.split (self.config)[0])[0], "certifications")
				certfile = os.path.join (_certpath, certfile)
				assert os.path.isfile (certfile), "cert file not found"					
			if keyfile and not os.path.isfile (keyfile):
				keyfile = os.path.join (_certpath, keyfile)
				assert os.path.isfile (keyfile), "key file not found"
			
			self.config_certification (certfile, keyfile, config.getopt ("ssl", "passphrase"))
			self.ssl_server = True
		
		if config.getopt ("proxy", "enable_proxy") == "yes":
			self.wasc.logger ("server", "----------------------------------------------------", "warn")
			if self.ssl_server:				
				self.wasc.logger ("server", "HTTP/HTTPS proxy service is disabled", "warn")
				self.wasc.logger ("server", "Proxy cannot be enabled with SSL", "warn")
				config.setopt ("server", "enable_proxy", "no")
			else:	
				self.wasc.logger ("server", "HTTP/HTTPS proxy service is enabled", "warn")
				self.wasc.logger ("server", "Proxy is for testing purpose only, check your config", "warn")
			self.wasc.logger ("server", "----------------------------------------------------", "warn")

		self.config_cachefs (
			config.getopt ("proxypass", "cache_dir", os.path.join (self.varpath, "cache")),
			config.getint ("proxypass", "cache_memory", 8),			
			config.getint ("proxypass", "cache_disk", 0),
		)
		self.config_rcache (config.getint ("tunefactors", "num_result_cache_max", 1000))
		
		# spawn
		self.config_webserver (
			config.getint ("server", "port", 5000),
			config.getopt ("server", "ip"),
			config.getopt ("server", "name"),
			config.getopt ("ssl", "enable_ssl") in ("yes", "1") or False,
			config.getint ("tunefactors", "keep_alive", 5),
			config.getint ("tunefactors", "response_timeout", 10)
		)
		
		# after spawn	
		self.config_threads (config.getint ("server", "threads", 4))
		for sect in list(config.keys ()):
			if sect.startswith ("@"):
				name = sect [1:]
				policy = AccessPolicy (
					config.getopt (sect, "roles", ""), 
					config.getopt (sect, "ips", "")
				)	
				members = [_f for _f in [x.strip () for x in config.getopt (sect, "members").split (",")] if _f]
				self.add_cluster (
					config.getopt (sect, "type"), 
					name, 
					members, 
					config.getopt (sect, "ssl"),
					policy
				)
		
		self.install_handler (
			config.getopt ("routes"), 
			config.getopt ("proxy", "enable_proxy") == "yes",			
			config.getint ("tunefactors", "static_max_age", 300),
			config.getopt ("etc", "blacklist_dir", None),
			config.getopt ("proxy", "enable_hacked_https") == "yes",
			config.getopt ("api-gateway", "enable_gateway") == "yes",
			config.getopt ("api-gateway", "authenticate") == "yes",
			config.getopt ("api-gateway", "realm", "API Gateway"),
			config.getopt ("api-gateway", "secret_key")
		)

		lifetime.init ()
		if os.name == "nt":			
			self.flock = flock.Lock (os.path.join (self.varpath, "lock"))
			self.flock.unlockall ()
			lifetime.maintern.sched (10.0, self.maintern_shutdown_request)

	def maintern_shutdown_request (self, now):
		req = self.flock.lockread ("signal")
		if not req: return
		self.wasc.logger ("server", "[info] got signal - %s" % req)
		if req == "terminate":			
			lifetime.shutdown (0, 1.0)
		elif req == "restart":			
			lifetime.shutdown (3, 30.0)		
		elif req == "shutdown":
			lifetime.shutdown (0, 30.0)		
		elif req == "rotate":
			self.wasc.logger.rotate ()
		else:
			self.wasc.logger ("server", "[error] unknown signal - %s" % req)
		self.flock.unlock ("signal")


def usage ():
		print("""
Usage:
	skitaid-instance.py [options...]

Options:
	--conf or -f [ea]/yekeulus
	--verbose or -v	
	--test: test configuration file
	--log=[server|app|request|stderr]: print log
	--help or -h

Examples:
	skitaid-instance.py -v -f default
	skitaid-instance.py -f default	
	skitaid-instance.py -f default -l server	
	""")


if __name__ == "__main__":
	argopt = getopt.getopt(sys.argv[1:], "f:hvtpl:", ["help", "conf=", "verbose", "test", "profile", "log="])
	_conf = ""
	_varpath = None
	_consol = False
	_test = False
	_profile = False
	_log = False
	
	for k, v in argopt [0]:
		if k == "--conf" or k == "-f":
			_conf = v
		elif k == "--verbose" or k == "-v":	
			_consol = True
		elif k == "--log" or k == "-l":	
			_log = v	
		elif k == "--profile" or k == "-p":	
			_profile = True	
		elif k == "--test" or k == "-t":	
			_test = True	
		elif k == "--help" or k == "-h":	
			usage ()
			sys.exit ()
	
	if not _conf:
		print("[error] config is required, use --conf or -f")		
		usage ()
		sys.exit (1)
		
	try:
		subdir, name = _conf.split ("/", 1)
	except ValueError:
		subdir, name = 	"e", _conf

	if subdir == "a":
		loc = "servers-available"
	elif subdir == "e":
		loc = "servers-enabled"
	else:
		print("[error] config type is unknown, should be e or a (default: e)")
		usage ()
		sys.exit (1)
	
	if name.endswith (".conf"):
		name = name [:-5]

	import skitaid	
	_config = os.path.join (skitaid.CONFIGPATH, loc, "%s.conf" % name)
	_varpath = os.path.join (skitaid.VARDIR, "instances", name)
	_logpath = os.path.join (skitaid.LOGDIR, "instances", name)
	
	if _log:
		if _log not in ("server", "request", "app", "stderr"):
			print("[error] no such log file '%s', should be one of server, app, request, stderr" % _log)
			usage ()
			sys.exit (1)
						
		skitaid.printlog (os.path.join (_logpath, "%s.log" % _log))
		sys.exit (0)
		
	if not (os.path.isfile (_config) or os.path.islink (_config)):
		print("[error] no server config file")
		usage ()
		sys.exit (1)
	
	if _test:
		WAS.test_config (_config)
		print("[ok] config file is good")
		sys.exit (0)
		
	lck = flock.Lock (os.path.join (_varpath, "lock"))
	pidlock = lck.get_pidlock ()
	
	if pidlock.isalive ():
		print("[error] instance '%s' already running" % _config)
		sys.exit (1)
	
	pathtool.mkdir (_logpath)
	if not _consol: # service mode
		from aquests.lib import devnull
		sys.stdout = devnull.devnull ()		
		sys.stderr = open (os.path.join (_logpath, "stderr.log"), "a")
	
	pidlock.make ()
	try:
		service = WAS (_config, _logpath, _varpath, _consol)
	except:
		tb = traceback ()
		if not _consol: # service mode
			sys.stderr.write (tb)	
			sys.stderr.flush ()
		else:
			print (tb)	
		sys.exit (0)		
	
	try:		
		service.run ((os.name == "nt" and _consol) and 2 or 30)
		
	finally:			
		_exit_code = service.get_exit_code ()
		if _exit_code is not None: # master process
			pidlock.remove ()
			if not _consol:
				sys.stderr.close ()	
			sys.exit (_exit_code)
		
		else: # worker process
			sys.exit (lifetime._exit_code)
	


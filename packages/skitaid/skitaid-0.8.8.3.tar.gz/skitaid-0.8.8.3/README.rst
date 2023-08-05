===============================
Skitai WSGI App Engine Daemon
===============================


This Package Had Been Deprecated
==================================

The reason why most of significant features was integrated with `Skitai App Engine`_ version 0.26, this package is no longer developed or mainterned any more.


.. contents:: Table of Contents


Introduce
===========

Skitai WSGI App Engine Deamon (SWAED) is an daemonizer using `Skitai App Engine`_.

SWAED is a kind of branch of `Medusa Web Server`__ - A High-Performance Internet Server Architecture.

Medusa is different from most other servers because it runs as a single process, multiplexing I/O with its various client and server connections within a single process/thread.

- HTTP/HTTPS Web, XML-RPC Server
- Loadbancing/Cache, API Gateway Server
- HTML5 Websocket Implemeted
- HTTP/2.0 Implemeted

Skitai also run with only Skitai App Engine, but This daemonizer has some benefits.

- Just Install and Run
- Configuration With Files
- Multiple Worker Processes (posix only)
- Multiple Domains
- Multiple Instances by Port Numbers
- Failover Recovery
- Async E-Mail Sending
- Job Scheduling

.. __: http://www.nightmare.com/medusa/medusa.html


What Can Skitai Specifically Do?
=================================

I'd like to provide some examples implementing microservice architecture.

**Microservice Server**

  Even Skitai can build legacy monolithic large app, but it is more suitable for microservice with light-weight machine like AWS' t2.nano or t2.micro instance.

**Loadbalancer & Caching Server**

  Some microservice servers or API gateway servers need loadbalancing or caching features, Skitai is useful.
  
  .. code-block:: bash
  
    [route:line]
    / = @microsoervice

    [@microservice]
    members = 172.31.0.1:5000, 172.31.0.2:5000
    
  This configuration will loadbalance for every requests to 2 microservice servers. Microservice developers may deply in front of their microservice servers.

**API Gateway Server**
  
  Every deployed microservices can be mapped with urls not network addresses.
  
  .. code-block:: bash
  
    [route:line]
    /users = @users
    /catalog = @catalog
    /catalog/inventory = @inventory

    [@users]
    # loadbalancer
    members = 172.31.0.1:5000
    
    [@catalog]
    # loadbalancer
    members = 172.31.0.2:5000
    
    [@inventory]
    # microserice servers directly
    members = 172.31.0.3:5000, 172.31.0.4:5000
  
  Then all clients to use microservice APIs just know microservice url.
  
  Each microservice aliases can point loadbalnacer or microservice server(s) for instant loadbalancing.

**BFF: Backends For Frontends**

  BFF_ is a pattern for implementing frontends with microservice architecture. It is some kind of orchestration model with HMTL, CSS, JS, images, session and microservices for frontends.
  
  Even most microservices can be called by javascript AJAX, but AJAX call for all microservices are not possible yet because like security and search engine optimization reasons. 
  
  Skitai's these features are proper to BFF_:
  
  - multiple parallel, timoutout-controlled RESTful API calling feature
  - cookie/session management
  - static files serving


.. _BFF: http://samnewman.io/patterns/architectural/bff/


Installation / Startup
=========================

**On Posix**

.. code-block:: bash

    sudo pip3 install --no-cache-dir skitaid
    
Option '--no-cache-dir' is should be given, otherwise installation is not working. I don't know why.

If you want to reinstall forcely,

.. code-block:: bash

    sudo pip3 install --no-cache-dir --upgrade --force skitaid


Another way from Git:

.. code-block:: bash

    git clone https://gitlab.com/hansroh/skitaid.git
    cd skitaid
    python setup.py install

For starting Skitai:

.. code-block:: bash
  
    sudo skitaid.py -v &
    sudo skitaid.py stop

    #if everythig is OK,
    
    sudo service skitaid start
    sudo service skitaid stop
    
    #For auto run on boot,
    sudo update-rc.d skitaid defaults
    or
    sudo chkconfig skitaid on


**On Win32**

.. code-block:: bash

    pip install skitaid
    
    cd c:\skitaid\bin
    skitaid.py -v
    skitaid.py stop (in another command prompt)
    
    #if everythig is OK,    
    install-win32-service.py install
    
    #For auto run on boot,
    install-win32-service.py --startup auto install    
    install-win32-service.py start
    install-win32-service.py stop


**Note For Win32 Python 3 Users**

Change python key value to like `c:\\python34\\python.exe` in c:\\skitaid\\etc\\skitaid.conf.


Mounting WSGI Apps and Static Directories
===========================================

Here's three WSGI app samples:

*WSGI App* at /var/wsgi/wsgiapp.py

.. code:: python
  
  def app (env, start_response):
    start_response ("200 OK", [("Content-Type", "text/plain")])
    return ['Hello World']


*Flask App* at /var/wsgi/flaskapp.py

.. code:: python

  from flask import Flask  
  app = Flask(__name__)  
  
  @app.route("/")
  def index ():	 
    return "Hello World"


*Skitai-Saddle App* at /var/wsgi/skitaiapp.py

.. code:: python

  from skitai.saddle import Saddle  
  app = Saddle (__name__)
  
  @app.route('/')
  def index (was):	 
    return "Hello World"

For mounting to SWAED, modify config file in /etc/skitaid/servers-enabled/example.conf

.. code:: python
  
  [routes:line]
  
  ; for files like images, css
  / = /var/wsgi/static
  
  ; app mount syntax is path/module:callable
  / = /var/wsgi/wsgiapp:app
  /aboutus = /var/wsgi/flaskapp:app
  /services = /var/wsgi/skitaiapp:app
  
You can access Flask app from http://127.0.0.1:5000/aboutus and other apps are same.


**Note: Mount point & App routing**

If app is mounted to '/flaskapp',

.. code:: python
   
  from flask import Flask    
  app = Flask (__name__)       
  
  @app.route ("/hello")
  def hello ():
    return "Hello"

Above /hello can called, http://127.0.0.1:5000/flaskapp/hello

Also app should can handle mount point. 
In case Flask, it seems 'url_for' generate url by joining with env["SCRIPT_NAME"] and route point, so it's not problem. Skitai-Saddle can handle obiously. But I don't know other WSGI middle wares will work properly.


Mounting With Virtual Host
===========================

*New in version 0.10.5*

App can be mounted with virtual host.

.. code-block:: bash

  [routes:line]
 
  / = /home/user/www/static
  / = /home/user/www/wsig:app
  
  
  # exactly matching host  
  @ www.mydomain.com mydomain.com 
     
  / = /home/user/mydomain.www/static
  /service = /home/user/mydomain.www/wsgi:app
  
  
  # matched *.mydomain.com include mydomain.com
  @ .mydomain.com
  
  / = home/user/mydomain.any/static 
  / = home/user/mydomain.any/wsgi:app 


  # matched *.mydomain2.com except mydomain2.com
  @ *.mydomain.com
  
  / = home/user/mydomain2.any/static 
  / = home/user/mydomain2.any/wsgi:app 


As a result, the app location '/home/user/mydomain.www/wsgi.py' is mounted to 'www.mydomain.com/service' and 'mydomain.com/service'.


API Gateway Server Access Control
==================================

Skitai as API Gateway Server does just 2 things: API routing, and access control by token validation, roles and IP addresses.

If you run Skitaid as API gateway server, there're many options for access control like IP address restriction or Basic/Digest authorization methods using key-password pair.

But Skitai only support API token based authorization methods for accessing API Gateway. And ID-Password authentificating, token generating, providing and storing process should be built in seperatly. API Gateway server just need some information about permisssion related things with token.

At configuration file,

.. code-block:: bash
  
  [api-gateway]
  enable_gateway = yes
  authenticate = yes
  realm = API Gateway
  secret_key = your_secret_key_for_JWT_authorization
  
  [route:line]
  / = /var/wsgi/example/gateway:app
  /users = @users
  /catalog = @catalog
  /catalog/inventory = @inventory

  [@users]
  # loadbalancer
  roles = user, admin
  members = 172.31.0.1:5000
  
  [@catalog]
  # loadbalancer
  roles = user, admin
  members = 172.31.0.2:5000
  
  [@inventory]
  # microserice servers directly
  roles = admin
  ips = 172.31.0.0/16
  members = 172.31.0.3:5000, 172.31.0.4:5000


/var/wsgi/example/gateway.py

.. code:: python

  from skitai.saddle import Saddle

  app = Saddle (__name__)
  app.debug = True
  app.use_reloader = True
  
  class Authorizer:
    def __init__ (self):
      self.tokens = {
        "12345678-1234-123456": ("hansroh", ["user", "admin"], 0)
      }
    
    # For Token	
    def handle_token (self, request, callback):
      username, roles, expires = self.tokens.get (request.token)
      if expires and expires < time.time ():
        self.tokens.popitem (request.token)
        return callback (request)
      callback (request, username, roles)
    
    # For JWT Claim
    def handle_claim (self, request, callback):
      claim = request.claim
      expires = claim.get ("expires", 0)
      if expires and expires < time.time ():
        return callback (request)
      callback (request, claim.get ("user"), claim.get ("roles"))
      
    
  @app.startup
  def startup (wasc):
    wasc.handler.set_auth_handler (Authorizer ())
  	
  @app.route ("/")
  def index (was):
  	return "<h1>API Gateway</h1>"

Object Tokens may be any object has handle_token or handle_claim with receiving args (request, callback) method. This method should call callback with request, username, roles. 

'handle_token' could get user information including username and roles by a token but it needn't for handle_claim. Because claim already contains access control information. If claim has at least 2 keys - 'user' and 'roles',  Skitai authorization works even no handle_claim method nor gateway initialization script like above '/var/wsgi/example/gateway.py'.

For more information about JWT visit JWT_ homepage.

.. _JWT: https://jwt.io/introduction/


Finally, your client is like this:

.. code:: python

  import requests
    
  requests.get (
    "http://127.0.0.1:5000/catalog/inventory/v1/status", 
    headers={"Authorization": "Bearer 12345678-1234-123456"}
  )

Or on your Saddle app:

.. code:: python

  @app.route ("/get")
  def get (was):
    s = was.get (
      "http://127.0.0.1:5000/catalog/inventory/v1/status", 
      auth = ("12345678-1234-123456",)
    )
    result = s.getwait (5)


Running Skitai as HTTPS Server
===============================

Simply config your certification files to config file (ex. /etc/skitaid/servers-enabled/example.conf). 

.. code:: python

  [ssl]
  enable_ssl = yes
  certfile = server.pem
  keyfile = server.key
  passphrase = fatalbug

To genrate self-signed certification file:

.. code:: python

    openssl req -new -newkey rsa:2048 -x509 -keyout server.pem -out server.pem -days 365 -nodes
    
For more detail please read README.txt in /etc/skitaid/certifications/README.txt


SMTP Delivery Agent
====================

e-Mail sending service is executed seperated system process not threading. Every e-mail is temporary save to file system, e-Mail delivery process check new mail and will send. So there's possibly some delay time.

You can send e-Mail in your app like this:

.. code:: python

    # email delivery service
    e = was.email (subject, snd, rcpt)
    e.set_smtp ("127.0.0.1:465", "username", "password", ssl = True)
    e.add_content ("Hello World<div><img src='cid:ID_A'></div>", "text/html")
    e.add_attachment (r"001.png", cid="ID_A")
    e.send ()

With asynchronous email delivery service, can add default SMTP Server config to skitaid.conf (/etc/skitaid/skitaid.conf or c:\skitaid\etc\skitaid.conf).
If it is configured, you can skip e.set_smtp(). But be careful for keeping your smtp password.

.. code:: python

    [smtpda]
    smtpserver = 127.0.0.1:25
    user = 
    password = 
    ssl = no
    max_retry = 10
    undelivers_keep_max_days = 30

Log file is located at /var/log/skitaid/daemons/smtpda/smtpda.log or c:\skitaid\log\daemons\smtpda\smtpda.log


Batch Task Scheduler
=====================

*New in version 0.14.5*

Sometimes app need batch tasks for minimum response time to clients. At this situateion, you can use taks scheduling tool of OS - cron, taks scheduler - or can use Skitai's batch task scheduling service for consistent app management. for this, add jobs configuration to skitaid.conf (/etc/skitaid/skitaid.conf or c:\\skitaid\\etc\\skitaid.conf) like this.

.. code:: python

  [crontab:line]
  
  */2 */2 * * * /home/apps/monitor.py  > /home/apps/monitor.log 2>&1
  9 2/12 * * * /home/apps/remove_pended_files.py > /dev/null 2>&1

Taks configuarion is same with posix crontab.

Cron log file is located at /var/log/skitaid/daemons/cron/cron.log or c:\skitaid\log\daemons\cron\cron.log


Skitai with Nginx / Squid
=============================

From version 0.10.5, Skitai supports virtual hosting itself, but there're so many other reasons using with reverse proxy servers.

Here's some helpful sample works for virtual hosting using Nginx / Squid.

If you want 2 different and totaly unrelated websites:

- www.jeans.com
- www.carsales.com

And make two config in /etc/skitaid/servers-enabled

- jeans.conf *using port 5000*
- carsales.conf *using port 5001*

Then you can reverse proxying using Nginx, Squid or many others.

Example Squid config file (squid.conf) is like this:

.. code:: python
    
    http_port 80 accel defaultsite=www.carsales.com
    
    cache_peer 192.168.1.100 parent 5000 0 no-query originserver name=jeans    
    acl jeans-domain dstdomain www.jeans.com
    http_access allow jeans-domain
    cache_peer_access jeans allow jeans-domain
    cache_peer_access jeans deny all
    
    cache_peer 192.168.1.100 parent 5001 0 no-query originserver name=carsales
    acl carsales-domain dstdomain www.carsales.com
    http_access allow carsales-domain
    cache_peer_access carsales allow carsales-domain
    cache_peer_access carsales deny all

For Nginx might be 2 config files (I'm not sure):

.. code:: python

    ; /etc/nginx/sites-enabled/jeans.com
    server {
	    listen 80;
	    server_name www.jeans.com;
      location / {
        proxy_pass http://192.168.1.100:5000;
      }
    }
    
    ; /etc/nginx/sites-enabled/carsales.com    
    server {
	    listen 80;
	    server_name www.carsales.com;
      location / {
        proxy_pass http://192.168.1.100:5001;
      }
    }


Configuration / Management
============================

Now let's move on to new subject about server configuration amd mainternance.

Configuration
--------------

Configuration files are located in '/etc/skitaid/servers-enabled/\*.conf', and on win32, 'c:\\skitaid\\etc\\servers-enabled/\*.conf'.

Basic configuration is relatively simple, so refer commets of config file. Current config file like this:

.. code:: python

  [server]
  threads = 4
  processes = 2
  ip = 127.0.0.1
  port = 5000
  name = 
  
  [ssl]
  enable_ssl = no
  certfile = server.pem
  keyfile = server.key
  passphrase = 
 
  [tunefactors]
  static_max_age = 300
  response_timeout = 10
  keep_alive = 10
  num_result_cache_max = 200
  
  [proxypass]
  cache_memory = 8
  cache_disk = 0
  
  [api-gateway]
  authenticate = no
  realm = API Gateway
    
  [routes:line]
  / = /var/wsgi/example/static
  / = /var/wsgi/example/webapp
  /about = @python
  
  [@python]
  ssl = yes
  members = www.python.org:443
  
  [@sqlite3]
  type = sqlite3
  members = /var/wsgi/example/resources/sqlite3.db


Here's configs required your carefulness.

- ip: default is 127.0.0.1 then you can only access to server via 127.0.0.1. If you want to access via public IP, set 0.0.0.0
- processes: number of workers but on Win32, only 1 is valid
- threads: generally not up to 4 per CPU. If set to 0, Skitai run with entirely single thread. so be careful if your WSGI function takes long time or possibly will be delayed by blocking operation.
- num_result_cache_max: number of cache for HTTP/RPC/DBMS results
- response_timeout: transfer delay timeout caused by network problem


Log Files
-----------

If Skitai run with skitaid.py, there're several processes will be created.

Sample ps command's result is:

.. code-block:: bash

  ubuntu:~/skitai$ ps -ef | grep skitaid
  root     19146 19145  0 Mar03 pts/0    00:00:11 /usr/bin/python /usr/local/bin/skitaid.py
  root     19147 19146  0 Mar03 pts/0    00:00:05 /usr/bin/python /usr/local/bin/skitaid-smtpda.py
  root     19148 19146  0 Mar03 pts/0    00:00:03 /usr/bin/python /usr/local/bin/skitaid-cron.py
  root     19150 19146  0 Mar03 pts/0    00:00:00 /usr/bin/python /usr/local/bin/skitaid-instance.py --conf=example

- /usr/local/bin/skitaid.py : Skitaid Daemon manages all Skitais sub processes
- /usr/local/bin/skitaid-instance.py : Skitai Instance with example.conf
- /usr/local/bin/skitaid-smtpda.py : SMTP Delivery Agent
- /usr/local/bin/skitaid-cron.py : Cron Agent

Skitai Daemon log file is located at:

- posix:  /var/log/skitaid/skitaid.log
- win32: c:\\skitaid\\log\\skitaid.log

To view latest 16Kb log,

  skitaid.py log

SMTP Delivery Agent log is located at:

- posix:  /var/log/skitaid/daemons/smtpda/smtpda.log
- win32: c:\\skitaid\\log\\daemons\\smtpda\\smtpda.log
- skitaid.py -f smtpda log

Cron Agent log is located at:

- posix:  /var/log/skitaid/daemons/cron/cron.log
- win32: c:\\skitaid\\log\\daemons\\cron\\cron.log
- skitaid.py -f cron log


If Skitai App Engine Instances config file is 'example.conf', log file located at:

- posix:  /var/log/skitaid/instances/example/[server|request|app].log
- win32: c:\\skitaid\\log\\instances\\example\\[server|request|app].log
- skitaid.py -f cron -s [server|request|app] log

To view lateset log, 

.. code:: python

  skitaid.py -f example log

Above log is like this:

.. code:: python
  
  2016.03.03 03:37:41 [info] called index
  2016.03.03 03:37:41 [error] exception occured
  2016.03.03 03:37:41 [expt:bp1] <type 'exceptions.TypeError'>\
    index() got an unexpected keyword argument 't'\
    [/skitai/saddle/wsgi_executor.py|chained_exec|51]
  2016.03.03 03:37:41 [info] done index

Request Log Format
-------------------

Request log is like this:

.. code:: bash

  2016.12.30 18:05:06 127.0.0.1:1778 localhost:5000 GET / \
  HTTP/1.1 0 200 32970 \
  GTID-C3-R8 1000 - - \
  "Mozilla/5.0 (Windows NT 6.1;) Gecko/20100101 Firefox/50.0" \
  4ms 3ms

**Log Format**

- Date
- Time
- Client IP:Port
- Server Name:Port
- Method
- URL
- HTTP/Version
- HTTP Response Code
- Bytes Recv
- Bytes Send
- Global Transaction ID
- Local Transaction ID
- User Name: By WWW-Athentificate, If not available, mark to hypen
- Token: API Access Token, If not available, mark to hypen
- User Agent (Souble Quoted)
- Internal Request Handling & Running Time
- Content Sending Time


Links
======

- `GitLab Repository`_
- Bug Report: `GitLab issues`_

Change Log
==============
  
- 0.8.6.1 - license changed from BSD to MIT

- 0.8.6 - project name chnaged: Skitai App Engine => Skitai App Engine Daemon

- 0.8.5 - fix installation

- 0.8.2 - update examples related websocket

- 0.8 - add some examples at skitaid/wsgi/example

- 0.7 - Change Log Format

- 0.5 - default executable python become a python3

- 0.4

  * Server configurration file is changed. You should change it
  * On posix installation, should give option --no-cache-dir

- 0.3
 
  * Server configurration file is changed. You should change it
  * On posix installation, should give option --no-cache-dir

- 0.1 - seperated from `Skitai App Engine`_


.. _`GitLab Repository`: https://gitlab.com/hansroh/skitaid
.. _`GitLab issues`: https://gitlab.com/hansroh/skitaid/issues
.. _`Skitai App Engine`: https://pypi.python.org/pypi/skitai

  
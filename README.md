# IXPQos
IXP Qos Monitoring Framework. 

## Overview
For a general overview of the framework please read the article on [Namex IXP blog](https://www.namex.it/assessing-performance-and-qos-of-a-distributed-peering-platform/)

## Setup

### Requirements
The framework relies ont the `ping3` Python package. API server requires a working uWSGI/NGINX setup (see below), data backend is provided by InfluxDB2 with proper authentication mechanisms in place.

### Server side
In order to configure uWSGI you need the following file added to the base directory, a reference example will be given here:

**ixpqos.in**
```
[uwsgi]
module = wsgi:app
master = true
processes = 3

socket = /tmp/ixpqos.sock
chmod-socket = 660
vacuum = true
plugins = python3

die-on-term = true
```

**wsgi.py**
```
from ixpqos import app
  

if __name__ == "__main__":
    app.run()
```

Next, you will need to configure NGINX to proxy requests to uWSGI:

```
server {
        listen 80;
        server_name YOUR_SERVER_NAME_HERE;
        return 301 https://YOUR_SERVER_NAME_HERE;
}

server {
        listen 443 ssl default_server;
        server_name YOUR_SERVER_NAME_HERE;

        # SSL configuration
        
        ssl_certificate YOUR_CERTS_DIR;
        ssl_certificate_key YOUR_PRIVATE_KEYS_DIR;

        root /var/www/html;

        location /backend {
                rewrite  ^/backend/(.*) /$1 break;
                uwsgi_pass unix:///tmp/ixpqos.sock;
                include uwsgi_params;
        }
}


### Client side


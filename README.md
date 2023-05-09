# IXPQos
A simple Qos Monitoring Framework for geographically distributed IXP platforms. 

## Overview
For a general overview of the framework please read the article on [Namex IXP blog](https://www.namex.it/assessing-performance-and-qos-of-a-distributed-peering-platform/)

## Setup

### Platform setup
In our setup, a dedicated VLAN is defined over the peering platform, in order to keep probe traffic segregated and not to waste public IP addresses. Probes are distributed at data centre sites and connected to the monitoring VLAN. The collector server is also connected to the VLAN and exposes its services via HTTP/REST.

### Software requirements
The framework relies on the following Python packages, suggestion is to setup a virtual environment and install them accordingly :

- ping3
- flask
- uwsgi
- influxdb_client
- requests 

After setting up the environment you can install the required packages by running:
```commandline
pip install -r requirements.txt
```
You will also need a working installation of InfluxDB2, with an organization, bucket and authentication token setup on purpose. Restful API requests are managed by a web server (NGINX in our case) and proxied to uWSGI, see the following section for details.

### Server host setup
In order to configure uWSGI you need the following file added to the base directory (ex. `/srv/IXPQos`), a reference example will be given here:

**ixpqos.ini**
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
In the same directory, add the following:

**wsgi.py**
```
from ixpqos import app
  

if __name__ == "__main__":
    app.run()
```

Next, you will need to configure NGINX to proxy requests to uWSGI, as in this example:

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
```
### IXPQos server configuration
You will need to craft your own application configuration file `config.py` and add it to directory `ixpqos/app`:

**config.py**
``` 
APP_CONFIG = {
    "apikey": YOUR_API_KEY,
    "bucket": YOUR_INFLUXDB_BUCKET,
    "org": YOUR_INFLUXDB_ORG,
    "token": YOUR_INFLUXDB_TOKEN,
    "url": "http://localhost:8086",
    "logfile": YOUR_LOG_FILE_PATH,
    "probes": "/etc/ixpqos/probes.json",
    "schedule": "/etc/ixpqos/schedule.json"
}
``` 
NOTE: the schedule mechanism is not supported yet. After creating configuration directory `/etc/ixpqos`, write down file `/etc/ixpqos/probes.json`, which should list all active probes in the system as in here:

***probes.json***
```
{
  "probes": [
    {
      "name": "p1-ixpqos",
      "proto": 4,
      "address": "10.0.0.1"
    },
    {
      "name": "p2-ixpqos",
      "proto": 4,
      "address": "10.0.0.2"
    },
    {
      "name": "p3-ixpqos",
      "proto": 4,
      "address": "10.0.0.3"
    }
  ]
}
```

### Client side
On client machine, you just need a running python environment with `ping3` package installed. You will schedule the **xprobe** util to run every five minutes (or according to your preferences) as in the following crontab line:
```
*/5 * * * * /srv/IXPQos/venv/bin/python3 /srv/IXPQos/utils/xprobe.py -k YOUR_API_KEY -n YOUR_PROBE_NAME -r YOUR_SERVER_NAME
```

## Operations
As soon as everything is in place, data collected from probes will be stored into the InfluxDB bucket, applications can be instructed to extract data and performs desired tasks as described in the [blog article](https://www.namex.it/assessing-performance-and-qos-of-a-distributed-peering-platform/).

## Support
This tool is provided as-is and without warranty as to its features, functionality, performance or integrity. The tool is currently operational at [Namex Roma IXP](https://www.namex.it), feel free to contact me if you want to give it a try and need help to setup the framework.
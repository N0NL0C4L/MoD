 Master of DDoS
==============

A simple and customizable HTTP flooder written in Python 3.

Features
--------

* Multi-threading
* Proxy support
* UserAgent randomization
* Customizable request method
* Customizable request amount

Requirements
------------

* Python 3.x
* `colorama`
* `fake_useragent`
* `socks`

Usage
-----

```
python3 mod.py -h
```

```
optional arguments:
  -h, --help            show this help message and exit
  --host                target host
  -p, --port            target port [default 80]
  -t, --thread          thread amount [default 100]
  -a, --amount          request amount [default inf]
  -m, --method          request method [default GET]
  -pl, --proxy-list      proxy list file
  -pt, --proxy-type      proxy type [default HTTP]
```

Examples
--------

### Simple HTTP GET Flood

```
python3 mod.py --host example.com -t 100 -a 1000000
```

### HTTP POST Flood with Proxy

```
python3 mod.py --host example.com -t 100 -a 1000000 -m POST -pl http_proxy_list.txt -pt HTTP
```

Disclaimer
----------

This tool is intended for educational purposes only. Using it for illegal activities is strictly prohibited. The author is not responsible for any misuse of this tool.

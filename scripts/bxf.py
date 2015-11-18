#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# by @aetsu
#
# Use: bxf.py url <payloads dictionary>
#

import mechanize
import sys


url = sys.argv[1]

if len(sys.argv) < 3:
    payloads = ['<script>alert(1);</script>']
else:
    filename = sys.argv[2]
    payloads = [line.rstrip('\n') for line in open(filename)]


# mechanize options
br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; \
    en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


try:
    br.open(url)
    print ""
    print ""
    print "                 BXF (Basic XSS finder)"
    print ""
    print "                                                     by @aetsu"
    print ""
    print "Url : " + url
    print "Testing payloads..."
    print ""
    for payload in payloads:
        for f in br.forms():
            br.select_form(nr=0)
            for idx, c in enumerate(br.controls):
                if br.controls[idx].type == "text":
                    br.form[br.controls[idx].name] = payload
        try:
            res = br.submit()
            content = res.read()

            if '<script>alert(1);</script>' in content:
                print "The form:"
                print f
                print "is possibly vulnerable!"
                print "Payload -> " + payload
                print ""
                break
        except:
            print "Error, testing next payload"
            continue
        try:
            br.open(url)
        except:
            print "Error opening " + url
            break
except:
    print "Error opening " + url

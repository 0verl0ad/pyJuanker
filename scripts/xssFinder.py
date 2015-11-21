#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# by @aetsu
#
# Use: xssFinder.py url <payloads dictionary>
#
import re
import urlparse
import mechanize
import requests
import sys


def getUrls(tarurl):
    urls = []

    print (" [+] Finding urls....")
    url = requests.get(tarurl)
    urls.append(str(tarurl))
    for u in re.findall('''href=["'](.[^"']+)["']''', url.text, re.I):
        try:
            if u[:4] == "http":
                if tarurl in u:
                    urls.append(str(u))
            elif u[0] == "/":
                combline = tarurl + u
                urls.append(str(combline))
            else:
                combline = tarurl + '/' + u
                urls.append(str(combline))
        except:
            pass

    return urls


def findXss(urls, payloads):
    for url in urls:

        # finding xss in url
        parsed = urlparse.urlparse(url)
        parameters = urlparse.parse_qs(parsed.query)
        newurl = urlparse.urljoin(parsed.scheme + "://" + parsed.netloc, parsed.path)

        print ""
        print " -> Url : " + url

        for payload in payloads:
            for p in parameters:
                parameters[p] = payload

            try:
                req = requests.get(newurl, params=parameters)
                if payload in req.text:
                    print chr(27) + "[1;31m" + "     The url " + chr(27) + "[0m" + url
                    print chr(27) + "[1;31m" + "     is possibly vulnerable!" + chr(27) + "[0m"
                    print "     Payload: " + payload
                    break

            except:
                print " <- Error opening " + url
                break

        # finding xss in forms
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
            print " "
            print "   Testing payloads in forms..."
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

                    if payload in content:
                        print chr(27) + "[1;31m" + "     The form:" + chr(27)+"[0m"
                        print f
                        print chr(27) + "[1;31m" + "     is possibly vulnerable!" + chr(27)+"[0m"
                        print "     Payload -> " + payload
                        print ""
                        break
                except:
                    continue
                try:
                    br.open(url)
                except:
                    print " <- Error opening " + url
                    break
        except:
            print " <- Error opening " + url

        print '==========================================================='
        print ''


def main():
    print ""
    print ""
    print "                 XSS finder"
    print ""
    print "                                                     by @aetsu"
    print ""
    if len(sys.argv) < 3:
        payloads = ['<script>alert(1);</script>']
    else:
        filename = sys.argv[2]
        payloads = [line.rstrip('\n') for line in open(filename)]

    urls = getUrls(sys.argv[1])
    findXss(urls, payloads)


if __name__ == "__main__":
    main()

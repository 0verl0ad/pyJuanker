#!/usr/bin/env python2
# by @aetsu
import socket
import sys
from multiprocessing.pool import Pool
import argparse

#iniPort = 1
#endPort = 65535
ip = ''


def scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print "Port open:-->\t", port
        sock.close()

    except socket.gaierror:
        print "Hostname could not be resolved"
        sys.exit()

    except socket.error:
        print "Could not connect to server"
        sys.exit()


def main():
    parser = argparse.ArgumentParser(description='portScan.py')
    parser.add_argument("-ip", dest="ip", help="ip to scan")
    parser.add_argument("-i", dest="iniPort", help="initial port ")
    parser.add_argument("-e", dest="endPort", help="end port")

    params = parser.parse_args()

    ip = str(params.ip)

    print('[+] Scanned IP -> ' + ip)
    print('\t' + str(params.iniPort) + ' - ' + str(params.endPort))

    p = Pool(50)
    p.map(scan, range(int(params.iniPort), int(params.endPort)))

if __name__ == '__main__':
    main()

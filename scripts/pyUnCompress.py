#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by @aetsu
import zipfile
import rarfile
import optparse
from threading import Thread

ALIVE = True


def extractFile(f, password):
    try:
        f.extractall(pwd=password)
        print '[+] Found password ' + password + '\n'
        global ALIVE
        ALIVE = False
    except:
        pass


def main():
    parser = optparse.OptionParser("Usage: pyUnCompress.py " +
                                   "-f <zipfile | rarfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string',
                      help='specify zip | rar file')
    parser.add_option('-d', dest='dname', type='string',
                      help='specify dictionary file')
    (options, args) = parser.parse_args()

    if (options.zname == None) | (options.dname == None):
        print parser.usage
        exit(0)
    else:
        zname = options.zname
        dname = options.dname

    flag = 0  # filetype -- rar = 1 | zip = 2

    if (rarfile.is_rarfile(zname)):
        compressFile = rarfile.RarFile(zname)
    elif (zipfile.is_zipfile(zname)):
        compressFile = zipfile.ZipFile(zname)
    else:
        print 'Unrecognized file'
        exit(0)

    passFile = open(dname)

    for line in passFile.readlines():
        if (ALIVE == False):
            exit(0)
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(compressFile, password))
        t.start()

if __name__ == '__main__':
    main()

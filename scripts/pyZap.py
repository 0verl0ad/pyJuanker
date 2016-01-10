#!/usr/bin/env python2
# -*- coding: utf-8 -*-

##########################################
# by @aetsu
# last update 11-01-2016
# tested on ZAP Weekly D-2015-12-29
# API version v2.4 0.0.7 (2015-12-10)
##########################################


import os
import sqlite3
import time
import sys
import argparse
import subprocess
from zapv2 import ZAPv2


class DataB:

    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.firstTime(dbname)

    def firstTime(self, dbname):
        '''
        Initialize database
        '''
        if os.path.exists(dbname):
            c = self.conn.cursor()
            # Create table
            c.execute('''CREATE TABLE vulnerabilities
                            (risk text, alert text, url text,
                            description text, solution text, param text)''')
            c.execute('''CREATE TABLE summary
                            (host text, number_of_alerts integer,
                            numberUrl integer, zapVersion text)''')
            c.execute('''CREATE TABLE urls
                            (url text)''')
            self.conn.commit()
        else:
            print('')
            print(
                chr(27) + "[1;31m" + "[+] Error, can't open database   :(   " +
                chr(27) + "[0m"
            )
            print('')
            sys.exit()

    def insertUrl(self, url):
        '''
        Insert a URL into database
        '''
        values = [(url,)]
        c = self.conn.cursor()
        c.executemany(
            'INSERT INTO urls VALUES(?)', values
        )
        self.conn.commit()

    def insertVuln(self, alert):
        '''
        Insert a vulnerability into database
        '''
        values = [(
            alert['risk'], alert['alert'], alert['url'],
            alert['description'], alert['solution'], alert['param']
        )]
        c = self.conn.cursor()
        c.executemany(
            'INSERT INTO vulnerabilities VALUES(?, ?, ?, ?, ?, ?)', values
        )
        self.conn.commit()

    def insertSummary(self, data):
        '''
        Insert info for the summary
        '''
        values = [(
            data['host'], data['number_of_alerts'],
            self.getNumberUrl(), data['zapVersion']
        )]
        c = self.conn.cursor()
        c.executemany(
            'INSERT INTO summary VALUES(?, ?, ?, ?)', values
        )
        self.conn.commit()

    def getNumberUrl(self):
        '''
        Get the number of URL in the database
        '''
        c = self.conn.cursor()
        c.execute('SELECT * FROM urls')
        return len(c.fetchall())

    def getSummary(self):
        '''
        Get the summary
        '''
        c = self.conn.cursor()
        c.execute('SELECT * FROM summary')
        return c.fetchone()

    def getVulnerabilities(self):
        '''
        Get the list of vulnerabilities
        '''
        c = self.conn.cursor()
        c.execute('SELECT * FROM vulnerabilities order by risk DESC')
        return c.fetchall()

    def closeCon(self):
        '''
        Close the database connection
        '''
        self.conn.close()


class ZapScanner:
    '''
    A class to interact with ZAP
    '''
    def __init__(self, url, dbname, apik):
        self.data = []
        # If ZAP is not listening on 8090
        # self.zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8080',
        #   'https': 'http://127.0.0.1:8090'})
        self.zap = ZAPv2()
        self.zap.core.new_session(overwrite='yes', apikey=apik)
        self.target = url
        self.db = DataB(dbname)
        self.apik = apik

    def z_openUrl(self):
        '''
        Load an URL in ZAP
        '''
        print(
            chr(27) + "[1;36m" + '[->>]' + chr(27) + "[0m" +
            '  Accessing target %s' % self.target
        )

        self.zap.urlopen(self.target)
        time.sleep(2)

    def z_spider(self):
        '''
        ZAP Spider
        '''
        print(
            chr(27) + "[1;36m" + '[->>]' + chr(27) + "[0m" +
            '  Spidering target %s' % self.target
        )
        self.zap.spider.scan(self.target, apikey=self.apik)
        # Give the Spider a chance to start
        time.sleep(2)
        '''
        first = ''

        while (int(self.zap.spider.status()) < 100):
            if first != self.zap.spider.status():
                print(
                    '         Spider progress: ' +
                    str(self.zap.spider.status()) + '%'
                )
            first = self.zap.spider.status()
            time.sleep(2)
        '''
        print(
            chr(27) + "[1;36m" + '[<<-]' +
            chr(27) + "[0m" + '  Spider completed'
        )
        # Give the passive scanner a chance to finish
        time.sleep(5)

    def z_ajaxSpider(self):
        '''
        ZAP ajaxSpider
        '''
        print(
            chr(27) + "[1;36m" + '[->>]' + chr(27) + "[0m" +
            '  AjaxSpider target %s' % self.target
        )
        self.zap.ajaxSpider.scan(self.target, apikey=self.apik)
        # Give the ajaxSpider a chance to start
        time.sleep(5)

    def z_ascan(self):
        '''
        ZAP active scan
        '''
        print(
            chr(27) + "[1;36m" + '[->>]' + chr(27) + "[0m" +
            '  Scanning target %s' % self.target
        )
        self.zap.ascan.scan(self.target, apikey=self.apik)
        '''
        while (self.zap.ascan.status() < 100):
            print(
                '         Scan progress: ' + str(self.zap.ascan.status()) + '%'
            )
        '''
        time.sleep(2)
        print(
            chr(27) + "[1;36m" + '[<<-]' + chr(27) + "[0m" + '  Scan completed'
        )
        self.z_insertDb()

    def z_insertDb(self):
        '''
        Insert relevant info in DB
        '''
        for url in self.zap.core.urls:
            self.db.insertUrl(url)

        for element in self.zap.core.alerts():
            self.db.insertVuln(element)

        data = {
            'host': ', '.join(self.zap.core.hosts),
            'number_of_alerts': self.zap.core.number_of_alerts(),
            'zapVersion': self.zap.core.version
        }
        self.db.insertSummary(data)

    def z_print_report(self):
        '''
        Print a summary
        '''
        summary = self.db.getSummary()
        vulnerabilities = self.db.getVulnerabilities()

        print('')
        print('')
        print('''
                                   __________
                     ______ ___.__.\____    /____  ______
                     \____ \   |  |  /     /\__  \ \____ \

                     |  |_| |___  | /     /_ / __ \|  |_| |
                     |   __// ____|/_______ (____  /   __/
                     |__|   \/             \/    \/|__|

            ''')
        print('                                     by @aetsu')
        print('')
        print('                                     Zap version ' + summary[3])
        print('')
        print('')
        print(
            chr(27) + "[1;35m" + '[Summary]' + chr(27) + "[0m"
        )

        print(
            chr(27) + "[1;35m" + '[->]' + chr(27) + "[0m" + '  Hosts: ' +
            summary[0]
        )
        print(
            chr(27) + "[1;35m" + '[->]' + chr(27) + "[0m" +
            '  Number of analized URLs: ' + str(summary[2]) +
            ' urls'
        )
        print(
            chr(27) + "[1;35m" + '[->]' + chr(27) + "[0m" +
            '  Number of alerts: ' + str(summary[1]) +
            ' alerts'
        )
        print(chr(27) + "[1;35m"' > Alerts:' + chr(27) + "[0m")

        for element in vulnerabilities:
            print('  [->]  ' + element[1])
            if element[0] == 'Medium':
                print(
                    '           Level: ' + chr(27) + "[1;33m" +
                    element[0] + chr(27) + "[0m"
                )
            elif element[0] == 'Low':
                print(
                    '           Level: ' + chr(27) + "[1;32m" +
                    element[0] + chr(27) + "[0m"
                )
            else:
                print(
                    '           Level: ' + chr(27) + "[1;31m" +
                    element[0] + chr(27) + "[0m"
                )
            print('           Url: ' + element[2])

    def z_dbClose(self):
        self.db.closeCon()

    def z_close(self):
        self.zap.core.shutdown()


def main():
    parser = argparse.ArgumentParser(description='  pyZap')
    parser.add_argument("-u", dest="url", help="url to scan")
    parser.add_argument("-d", dest="db", help="database name")
    parser.add_argument("-a", dest="api", help="ZAP api key (needs to start)")
    parser.add_argument("-daemon", dest="daemon",
                        action='store_true', help="starts zap as a daemon")

    params = parser.parse_args()

    if not params.api:
        parser.print_help()
        sys.exit()
    else:
        apik = params.api

    target = str(params.url)
    if not params.url:
        parser.print_help()
        sys.exit()
    elif target.find('http') == -1:
        target = 'http://' + target

    if not params.db:
        dbname = 'session.' + time.ctime().replace(' ', '_') + '.db'
    else:
        dbname = str(params.db)

    if params.daemon:
        # needs to change to your zap path
        zapPath = 'ZAP_2.4.3/zap.sh'
        subprocess.Popen([zapPath, '-daemon'], stdout=open(os.devnull, 'w'))
        print('Waiting for ZAP...')
        time.sleep(20)

    z = ZapScanner(target, dbname, apik)
    print(
        chr(27) + "[1;36m" + '[Target -> ' + target + ']' + chr(27) + "[0m"
    )
    z.z_openUrl()
    z.z_spider()
    # z.z_ajaxSpider()
    z.z_ascan()
    z.z_print_report()
    z.z_dbClose()

    if params.daemon:
        print('Shutdown ZAP')
        z.z_close()

if __name__ == '__main__':
    main()

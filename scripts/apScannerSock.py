#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# by @aetsu
import socket
import sys
import os
import signal
import random
import time
from multiprocessing import Process

interface = 'mon0'


def channel_hopper():
    """
    Channel hopper
    """
    while True:
        try:
            channel = random.randrange(1, 13)  # 13 canales legales en europa
            os.system("iw dev %s set channel %d" % (interface, channel))
            time.sleep(1)
        except KeyboardInterrupt:
            break


def signal_handler(signal, frame):
    """
    Captures CTRL+C interruption
    """
    p.terminate()
    p.join()
    sys.exit(0)


if __name__ == "__main__":
    p = Process(target=channel_hopper)
    p.start()

    signal.signal(signal.SIGINT, signal_handler)

    sniff = socket.socket(
        socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003)
    )

    sniff.bind((interface, 0x0003))
    aps = []

    while True:
        fm = sniff.recvfrom(4069)[0]

        if fm[36] == "\x80":  # beacon frame x80
            ssidLen = ord(fm[73])  # SSID length
            if fm[46:52] not in aps and ssidLen > 0:
                aps.append(fm[46:52])  # mac is added to list

                print(
                    "ESSID: %s \t BSSID: %s \t CHANNEL: %d" %
                    (fm[74:74 + ssidLen],
                        fm[46:52].encode('hex'),
                        (ord(fm[86 + ssidLen])))
                )

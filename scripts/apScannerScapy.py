#!/usr/bin/env python2
# by @aetsu
import sys
import os
import signal
from multiprocessing import Process
from scapy.all import *

interface = 'mon0'  # monitor interface
aps = []


def captura(p):
    """
    Filter only Deauth packets
    """
    if ((p.haslayer(Dot11Beacon))):
        if p[Dot11].addr3 not in aps:
            aps.append(p[Dot11].addr3)
            print(
                "ESSID: %s \t BSSID: %s \t CHANNEL: %d" %
                (p[Dot11].info, p[Dot11].addr3,
                    int(ord(p[Dot11Elt:3].info)))
            )


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
    Capturres the CTRL+C interruption
    """
    p.terminate()
    p.join()
    sys.exit(0)

if __name__ == "__main__":
    p = Process(target=channel_hopper)
    p.start()

    signal.signal(signal.SIGINT, signal_handler)

    sniff(iface=interface, prn=captura)

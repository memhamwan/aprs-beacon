#!/usr/bin/env python

from datetime import datetime
import socket
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import yaml


def aprs_dict_to_string(dict):
    dict['time'] = datetime.utcnow().strftime("%d%H%M")
    dict['name'] = dict['name'].ljust(9)
    return ";%(name)s*%(time)sz%(lat)sN/%(lon)sWr%(comment)s" % dict

registry = CollectorRegistry()

with open(r'./config/settings.yml') as file:

    data = yaml.load(file, Loader=yaml.SafeLoader)

    objs = data['objects']

    APRS_SERVER_HOST = data['server']
    APRS_SERVER_PORT = data['port']
    APRS_USER = data['user']
    APRS_PASSCODE = data['passcode']

    # create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((APRS_SERVER_HOST, APRS_SERVER_PORT))
    sock.send(('user %s pass %s vers KD7LXL-Python 0.2\n' % (APRS_USER, APRS_PASSCODE)).encode() )
    g = Gauge('aprs_packet_length', 'Length of the APRS packets', ['name'])

    for obj in objs:
        packet = "%s>APRS:%s\n" % (APRS_USER, aprs_dict_to_string(obj))
        sock.send(packet.encode())
        g.labels(obj['name']).set(len(packet))

    # close socket -- must be closed to avoid buffer overflow
    sock.shutdown(0)
    sock.close()

    g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)
    g.set_to_current_time()
    if 'prometheus' in data.keys():
        push_to_gateway(data['prometheus']['host'], job = data['prometheus']['job'], registry=registry) #TODO: move this to a config file

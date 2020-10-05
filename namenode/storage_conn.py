import requests as r
from .exceptions import *

def post(ip, uri, data):
    try:
        x = r.post(f'http://{ip}/' + uri, json=data)
        try:
            return x.json()
        except ValueError:
            raise NodeDisconnected()
    except r.exceptions.ConnectionError:
        raise NodeDisconnected()

def get(ip, uri):
    try:
        x = r.get(f'http://{ip}/' + uri)
        try:
            return x.json()
        except ValueError:
            raise NodeDisconnected()
    except r.exceptions.ConnectionError:
        raise NodeDisconnected()

def create_new_file(node_ip, filename):
    data = {'filepath': filename}
    resp = post(node_ip, 'create_file', data)

def delete(node_ip, filename):
    post(node_ip, 'delete', data={'path': filename})

def ping_node(node_ip):
    get(node_ip, 'ping')

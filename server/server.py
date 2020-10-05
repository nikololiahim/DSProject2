import socket
import requests
from flask import Flask, request
import os
import psutil


class Server:
    def __init__(self, server_ip, files_per_dir):
        ###
        # server_ip: String; NameNode ip address
        # files_per_dir: Integer; Number of files allowed per directory
        ###
        self.working_dir = 'root'
        self.server_ip = server_ip
        hostname = socket.gethostname()
        self.IP = socket.gethostbyname(hostname)
        self.files_per_dir = files_per_dir
        self.connected = False

    def connect_to_server(self):
        req = requests.get('https://' + self.server_ip + '/connect/')
        i = 1
        while req.status_code != 200 and i < 3:
            data = {'size': psutil.disk_usage('/')}
            req = requests.get('https://' + self.server_ip + '/connect/')
            i += 1
        self.connected = True

    def disconnect_from_server(self):
        req = requests.get('https://' + self.server_ip + '/disconnect/')
        i = 1
        while req.status_code != 200 and i < 3:
            req = requests.get('https://' + self.server_ip + '/disconnect/')
            i += 1
        self.connected = False


app = Flask(__name__)


class Foo:
    count = 0


f_cnt = Foo()


@app.route('/file', methods=['POST'])
def create_file():
    data = request.get_json()
    if data is None:
        return {'error': 'No file was sent'}, 400
    else:
        real_path = os.path.join('root', 'file', str(f_cnt.count))
        file = open(real_path)
        file.write(data['file'])
        file.close()
        f_cnt.count += 1
        return {'status': 'ok'}


@app.route('/del', methods=['DELETE'])
def delete_file():
    data = request.get_json()
    if data is None:
        return {'error': 'No file was sent'}, 400
    else:
        if os.path.exists(data['path']):
            os.remove(data['path'])
            return {'status': 'OK'}
        else:
            return {'error': 'File Does not exist'}, 400


@app.route('/upd', methods=['PUT'])
def update_file():
    data = request.get_json()
    if data is None:
        return {'error': 'No file was sent'}, 400
    else:
        if os.path.exists(data['path']):
            os.remove(data['path'])
            file = open(data['path'])
            file.write(data['file'])
            file.close()
            return {'status': 'OK'}
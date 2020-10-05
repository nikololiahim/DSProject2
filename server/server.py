import requests
import psutil
import os
from server.exceptions import DirDoesNotExist


class Server:
    def __init__(self, server_ip, working_dir=os.getcwd()):
        ###
        # server_ip: String; NameNode ip address
        # files_per_dir: Integer; Number of files allowed per directory
        ###
        if not os.path.isdir(working_dir):
            raise DirDoesNotExist()
        self.working_dir = working_dir
        self.server_ip = server_ip
        self.connected = False

    def connect_to_server(self):
        data = {'size': psutil.disk_usage('/').free}
        resp = requests.get('https://' + self.server_ip + '/connect/', data)
        i = 1
        while resp.status_code != 200 and i < 3:
            resp = requests.get('https://' + self.server_ip + '/connect/', data)
            i += 1
        self.connected = True
        if i <= 3:
            print('Connection Successful! Node id:' + str(resp.json()['id']))
        else:
            return {'error': 'Could not connect to the NameNode'}

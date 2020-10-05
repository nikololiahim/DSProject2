import requests
import os


class Client:
    NAME_NODE_URL = ""

    CORRUPTED_RESPONSE = 'The response from server is corrupted!'
    CONNECTION_ERROR = 'Connection with server is lost!'
    NO_NODE_AVAILABLE = 'No nodes are available to store this file!'
    NOT_ENOUGH_STORAGE = 'There is not enough memory to store your file!'
    NODE_DISCONNECTED = 'Node storing the file disconnected!'
    FILE_NOT_FOUND = 'File with such name was not found!'
    NO_SUCH_DIRECTORY = 'Directory with such name doesn\'t exist!'
    INTEGRITY_ERROR = 'One of the storage servers reported an integrity error!'

    CODE_CORRUPTED_RESPONSE = 400
    CODE_CONNECTION_ERROR = 418
    CODE_NO_NODE_AVAILABLE = 501
    CODE_NOT_ENOUGH_STORAGE = 502
    CODE_NODE_DISCONNECTED = 503
    CODE_FILE_NOT_FOUND = 504
    CODE_NO_SUCH_DIRECTORY = 505
    CODE_INTEGRITY_ERROR = 506

    error_dict = {
        CODE_CORRUPTED_RESPONSE: CORRUPTED_RESPONSE,
        CODE_CONNECTION_ERROR: CONNECTION_ERROR,
        CODE_NO_NODE_AVAILABLE: NO_NODE_AVAILABLE,
        CODE_NOT_ENOUGH_STORAGE: NOT_ENOUGH_STORAGE,
        CODE_NODE_DISCONNECTED: NODE_DISCONNECTED,
        CODE_FILE_NOT_FOUND: FILE_NOT_FOUND,
        CODE_NO_SUCH_DIRECTORY: NO_SUCH_DIRECTORY,
        CODE_INTEGRITY_ERROR: INTEGRITY_ERROR
    }

    def __init__(self, cwd):
        self.cwd = cwd

    def set_cwd(self, new_cwd):
        self.cwd = new_cwd

    def get_cwd(self):
        return self.cwd

    @staticmethod
    def post(uri, data):
        try:
            url = os.path.join(Client.NAME_NODE_URL, uri)
            x = requests.post(url, json=data)
            try:
                return x.json(), x.status_code
            except ValueError:
                return None, Client.CODE_CORRUPTED_RESPONSE
        except requests.exceptions.ConnectionError:
            return None, Client.CODE_CONNECTION_ERROR

    @staticmethod
    def response_failed(status_code):
        return Client.error_dict.get(status_code) is not None

    @staticmethod
    def handle_response(status_code):
        return Client.error_dict[status_code]

    @staticmethod
    def dfs_init():
        """
        Initialize the client storage on a new system,
        should remove any existing file in the dfs root
        directory and return available size.

        :returns size of available storage, set cwd to '/'
        """
        response, code = Client.post('dfs_init', data={})
        if response is None:
            return Client.handle_response(code)
        else:
            size = response['size']
            return f'Available size: {size} bytes' \
                   f' or {size / 1024} kilobytes or' \
                   f' {size / 1024 / 1024} megabytes or' \
                   f' {size / 1024 / 1024 / 1024} gigabytes.'

    @staticmethod
    def dfs_file_create(filename):
        """
        Allows to create a new empty file.
        """
        data = {'filename': filename}
        response, code = Client.post('dfs_file_create', data)
        if Client.response_failed(code):
            return Client.handle_response(code)
        else:
            node_ip = response['node_ip']
            return f'The new file with name \'{filename}\' was created at \'{node_ip}\'.'

    @staticmethod
    def dfs_file_read(filename):
        """
        Allows to read any file from DFS (download a file from the DFS to the Client side).
        """
        data = {'filename': filename}
        response, code = Client.post('dfs_file_read', data)
        if Client.response_failed(code):
            return Client.handle_response(code)
        else:
            data = {'path': filename}
            node_ip = response['node_ip']
            uri = os.path.join(node_ip, 'send')
            response, code = Client.post(uri, data)
            if Client.response_failed(code):
                return Client.handle_response(code)
            else:
                file = response.content
                with open(os.path.basename(filename), 'w') as out:
                    out.write(file)
                return f'File {filename} has been successfully downloaded!'

    @staticmethod
    def dfs_file_write(filename, size):
        """
        Allows to put any file to DFS (upload a file from the Client side to the DFS)
        """
        data = {'filename': filename,
                'size': size}
        response, code = Client.post('dfs_file_write', data)
        if Client.response_failed(code):
            return Client.handle_response(code)
        else:
            data = {'path': filename}
            node_ip = response['node_ip']
            uri = os.path.join(node_ip, 'rcv')
            _, code = Client.post(uri, data)
            if Client.response_failed(code):
                return Client.handle_response(code)
            else:
                return f'File was successfully uploaded to {node_ip}!'

    @staticmethod
    def dfs_file_delete(filename):
        """
        Should allow to delete any file from DFS
        """
        data = {'filename': filename}
        response, code = Client.post('dfs_file_delete', data)
        if Client.response_failed(code):
            return Client.handle_response(code)
        else:
            return f'File {filename} has been successfully deleted!'

    def dfs_file_info(self, filename):
        """
        Should provide information about the file (any useful information - size, node id, etc.)
        """

    def dfs_file_copy(self, filename, dest):
        """
        Should allow to create a copy of file.
        """

    def dfs_file_move(self, filename, dest):
        """
        Should allow to move a file to the specified path.
        """

    def dfs_dir_open(self, name):
        """
        Should allow to change directory
        """

    def dfs_dir_read(self, name):
        """
        Should return list of files, which are stored in the directory.
        """

    def dfs_dir_make(self, name):
        """
        Should allow to create a new directory.
        """

    def dfs_dir_delete(self, name):
        """
        Should allow to delete directory.  If the directory contains
        files the system should ask for confirmation from the
        user before deletion.
        """

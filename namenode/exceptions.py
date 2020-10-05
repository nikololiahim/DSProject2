from werkzeug.exceptions import HTTPException

class AmazingHTTPException(HTTPException):
    """
    Name of this class refers to TDD, don't mind
    """
    def __init__(self, description=None):
        if description is not None:
            self.description = description
        super().__init__(self.description, {'error': self.description})

class NodeUnavailable(AmazingHTTPException):
    code = 501
    description = 'No node available'

class NotEnoughStorage(AmazingHTTPException):
    code = 502
    description = 'Not enough storage'

class NodeDisconnected(AmazingHTTPException):
    code = 503
    description = 'Node disconnected'

class FileNotFound(AmazingHTTPException):
    code = 504
    description = 'File not found'

class DirectoryNotFound(AmazingHTTPException):
    code = 505
    description = 'Directory not found'

class IntegrityError(AmazingHTTPException):
    code = 506
    description = 'DFS Integrity Error'

class ServerError(AmazingHTTPException):
    code = 500
    description = 'Something went wrong (porbably DB)'


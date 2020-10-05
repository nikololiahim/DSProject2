from werkzeug.exceptions import HTTPException


class ServerConnectionError(Exception):
    """Server is not connected to the NameNode"""
    pass


class DirDoesNotExist(Exception):
    """Directory does not exist"""
    pass


class IntegrityError(HTTPException):
    code = 506
    description = "Integrity Error"


class FileNotFound(HTTPException):
    code = 504
    description = "File not found"

from sqlalchemy import Column, Integer, String, ForeignKey
from .settings import Base
from .settings import session
from sqlalchemy import func
from sqlalchemy import exc
from sqlalchemy.orm import query, relationship
from .storage_conn import *
from .exceptions import *


class FilesTable(Base):
    __tablename__ = 'files'
    storage_id = Column(Integer, primary_key=True)
    path = Column(String)
    size = Column(Integer)
    storage_rel = relationship('NodesTable', foreign_keys='FilesTable.storage_id')


class NodesTable(Base):
    __tablename__ = 'nodes'
    storage_id = Column(Integer, primary_key=True, autoincrement=True)
    storage_size = Column(Integer)
    addr = Column(String)


def create_object(obj):
    session.add(obj)
    try:
        session.commit()
        return obj
    except exc.IntegrityError:
        session.rollback()
        raise ServerError()


def get_available_size():
    return session.query(func.sum(NodesTable.storage_size)).scalar()


def add_node(addr, size):
    obj = NodesTable(storage_size=size, addr=addr)
    create_object(obj)
    return obj.storage_id


def get_most_free_node():
    """
    Сделать проверку на отсутствие ноды
    """
    return None


def create_file(filename):
    node = get_most_free_node()
    obj = FilesTable(storage_id=node.id, path=filename, size=0)
    create_new_file(node.addr, filename)
    create_object(obj)
    return obj.storage_id


def write_file(filename, size):
    """
    TODO: подумать над тем, что стоит создавать рекорды после фактической записи файла
    """
    node = get_most_free_node()
    if node.storage_size - size <= 0:
        raise NotEnoughStorage()
    obj = FilesTable(storage_id=node.id, path=filename, size=size)
    create_object(obj)
    node.storage_size -= size
    session.commit()
    return node.addr


def find_node_by_file(filename):
    res = session.query(FilesTable.storage_id).filter(FilesTable.path == filename)
    node = session.query(NodesTable).filter(NodesTable.storage_id == res[0])[0]
    return node


def delete_file(filename):
    res = session.query(FilesTable).filter(FilesTable.path == filename)
    for entry in res:
        node = session.query(NodesTable).filter(NodesTable.storage_id == entry.storage_id)[0]
        delete(node.addr, filename)
        node.storage_size -= entry.storage_id
    res.delete()
    session.commit()

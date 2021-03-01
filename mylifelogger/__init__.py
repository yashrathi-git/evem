from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from os.path import join as path_join


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()


def create_dir_if_not_exists(path: str, dirname: str) -> str:
    dir_path = path_join(path, dirname)
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
    return dir_path


BASEDIR = os.path.abspath(os.path.dirname(__file__))

create_dir_if_not_exists(BASEDIR, 'database')
DB_PATH = os.path.join(BASEDIR, 'database', 'data.sqlite')


engine = create_engine('sqlite:///'+DB_PATH)
Base = declarative_base()

_SessionFactory = sessionmaker(bind=engine)

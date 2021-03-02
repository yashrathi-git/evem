import configparser
import os
from os.path import join as path_join

from colorama import Fore, Style, init
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

init()

BASEDIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_LOCATION = os.path.abspath(os.path.join(BASEDIR, os.pardir, 'conf.ini'))

conf = configparser.ConfigParser()
warn = (f'{Fore.LIGHTYELLOW_EX}Please update email in conf.ini file to'
        f' receive reminders{Style.RESET_ALL}\n'
        f'Location for conf.ini file: {CONFIG_LOCATION}\n')

if not os.path.exists(CONFIG_LOCATION):
    conf['EMAIL_TO_SEND_REMINDERS'] = {}
    conf['EMAIL_TO_SEND_REMINDERS']['EMAIL'] = 'your_email@email.com'
    with open('conf.ini', 'w') as configfile:
        conf.write(configfile)
    print(warn)
    send_to = None
else:
    conf.read(CONFIG_LOCATION)
    send_to = conf['EMAIL_TO_SEND_REMINDERS']['EMAIL']
    if send_to == 'your_email@email.com':
        print(warn)
        send_to = None


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


create_dir_if_not_exists(BASEDIR, 'database')
DB_PATH = os.path.join(BASEDIR, 'database', 'data.sqlite')


engine = create_engine('sqlite:///'+DB_PATH)
Base = declarative_base()

_SessionFactory = sessionmaker(bind=engine)

import configparser
import os
from os.path import join as path_join

from colorama import Fore, Style, init
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


BASEDIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_LOCATION = os.path.abspath(os.path.join(BASEDIR, os.pardir, 'conf.ini'))
DB_PATH = os.path.join(BASEDIR, 'database', 'data.sqlite')


WARN = (f'{Fore.LIGHTYELLOW_EX}[WARNING]:Email to send reminder/notification not found, '
        f'run \nevem init\nto set it.{Style.RESET_ALL}')


def insert_into_config_email(email):
    conf = configparser.ConfigParser()
    conf['EMAIL_TO_SEND_REMINDERS'] = {}
    conf['EMAIL_TO_SEND_REMINDERS']['EMAIL'] = email
    with open(CONFIG_LOCATION, 'w') as configfile:
        conf.write(configfile)


def create_dir_if_not_exists(path: str, dirname: str) -> str:
    dir_path = path_join(path, dirname)
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
    return dir_path


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()


if not os.path.exists(CONFIG_LOCATION):
    insert_into_config_email('your_email@email.com')
    print(WARN)
    send_to = None
else:
    conf = configparser.ConfigParser()
    conf.read(CONFIG_LOCATION)
    send_to = conf['EMAIL_TO_SEND_REMINDERS']['EMAIL']
    if send_to == 'your_email@email.com':
        print(WARN)
        send_to = None


create_dir_if_not_exists(BASEDIR, 'database')


engine = create_engine('sqlite:///'+DB_PATH)
Base = declarative_base()

_SessionFactory = sessionmaker(bind=engine)
init()

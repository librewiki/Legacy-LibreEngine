__author__ = 'Wonwoo'
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from conf.database import *

engine = create_engine('mysql:libredev:libre_dev@sv3.al.gl/libredev', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
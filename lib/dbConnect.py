__author__ = 'Wonwoo'
from sqlalchemy import create_engine, Column, Integer, Text, Unicode
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from conf.database import *



engine = create_engine('mysql+pymysql://libredev:libre_dev@sv3.al.gl/libredev?charset=utf8', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class WikiPage(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    document = Column(Unicode(convert_unicode=True), unique=True)
    rev = Column(Integer)
    text = Column(Unicode(convert_unicode=True))
    date = Column(Integer)
    
    def __init__(self, document=None, rev=None, text=None, date=None):
        print(document)
        self.document = document
        self.rev = rev
        self.text = text
        self.date = date
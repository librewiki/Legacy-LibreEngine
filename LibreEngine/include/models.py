__author__ = '이츠레아'
from LibreEngine.lib.dbConnect import *

class WikiText(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.Unicode(convert_unicode=True), unique=True)
    rev = db.Column(db.Integer)
    text = db.Column(db.Unicode(convert_unicode=True))
    date = db.Column(db.Integer)




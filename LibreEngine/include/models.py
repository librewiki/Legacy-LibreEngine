__author__ = '이츠레아,nayuta'
from LibreEngine.lib.dbConnect import *
from flask import url_for



class WikiText(db.Model):

    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.Unicode(convert_unicode=True), unique=True)
    rev = db.Column(db.Integer)
    text = db.Column(db.Unicode(convert_unicode=True))
    date = db.Column(db.Integer)

def detour(page_role):
    editpage = str(page_role)
    detour = "<p>현재 " + editpage + "(은)는 아직 준비중입니다!</p>" + "<a href=" + url_for('main') + ">메인페이지</a>로 돌아가시겠습니까?"
    return detour
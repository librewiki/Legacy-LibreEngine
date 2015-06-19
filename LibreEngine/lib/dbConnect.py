__author__ = '이츠레아, 나유타'



from flask.ext.sqlalchemy import SQLAlchemy
from LibreEngine import app
from LibreEngine.conf.database import db_config

app.config["SQLALCHEMY_DATABASE_URI"] = db_config.KIND + "://" + db_config.USER + ":" + db_config.PASS + "@" + db_config.HOST + "/" + db_config.DATABASE + "?charset=utf8"
db = SQLAlchemy()
db.init_app(app)

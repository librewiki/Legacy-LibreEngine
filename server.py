__author__ = 'seyriz'


from LibreEngine.conf import config
from LibreEngine import app

app.run(config.default_config.HOST, config.default_config.PORT, config.default_config.DEBUG)
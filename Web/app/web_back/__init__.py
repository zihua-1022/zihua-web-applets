from flask import Flask
from web_back.views import equipment
from web_back.views import fileOpera
from web_back.views import image
from web_back.views import logs
from web_back.views import user
from web_back.common import config
from datetime import timedelta
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    app.wsgi_app=ProxyFix(app.wsgi_app)
    #注册蓝图，第一个参数userapp是蓝图对象，url_prefix参数默认值是根路由，
    #如果指定，会在蓝图注册的路由url中添加前缀。
    app.register_blueprint(user.userapp,url_prefix='/user')
    app.register_blueprint(image.imageapp,url_prefix='/image')
    app.register_blueprint(logs.logsapp,url_prefix='/logs')
    app.register_blueprint(equipment.equipapp,url_prefix='/equip')
    app.register_blueprint(fileOpera.fileoperaapp,url_prefix='/fileopera')
    return app

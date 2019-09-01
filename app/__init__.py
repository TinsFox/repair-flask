"""
    Created by TinsFox on 2019-08-19.
"""
from .app import Flask
from flasgger import Swagger

__author__ = 'TinsFox'


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()


def create_app(app):
    # app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    register_blueprints(app)
    register_plugin(app)
    # swagger_config = Swagger.DEFAULT_CONFIG
    # swagger_config['title'] = config.SWAGGER_TITLE  # 配置大标题
    # swagger_config['description'] = config.SWAGGER_DESC  # 配置公共描述内容
    # swagger_config['host'] = config.SWAGGER_HOST  # 请求域名
    #
    # # swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
    # # swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
    # # swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
    # # swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'
    # Swagger(app, config=swagger_config)
    return app

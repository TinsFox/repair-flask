"""
    Created by TinsFox on 2019-08-19.
"""
from werkzeug.exceptions import HTTPException
from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError
from flask.json import JSONEncoder as _JSONEncoder
from flask import Flask as _Flask
from datetime import datetime
from flask_cors import CORS
from flasgger import Swagger
__author__ = 'TinsFox'


# app = create_app()
class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d')
        return dict(o)


class Flask(_Flask):
    json_encoder = JSONEncoder


init_app = Flask(__name__)
CORS(init_app)
app = create_app(init_app)


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 调试模式
        # log
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# -*- coding: utf-8 -*- 
# @Time : 2019/11/29 1:52 下午 
# @Author : Lian 
# @Site :  
# @File : __init__.py

import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the parkingsys app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='de9dk0fslf78s^4$da',
        DATABASE=os.path.join(app.instance_path, 'data.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)  # 非正式部署可以忽略
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import parkingbp
    app.register_blueprint(parkingbp.bp)
    app.add_url_rule('/', endpoint='index')

    return app

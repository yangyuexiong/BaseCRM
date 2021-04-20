# -*- coding: utf-8 -*-
# @Time    : 2021/4/19 下午5:20
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Blueprint
from flask_restful import Api

from .login.login import LoginApi

route_api = Blueprint('api', __name__)
api = Api(route_api)

api.add_resource(LoginApi, '/login', endpoint='login')

api.init_app(route_api)

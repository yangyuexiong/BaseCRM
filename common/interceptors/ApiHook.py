# -*- coding: utf-8 -*-
# @Time    : 2020/7/21 3:49 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ApiHook.py
# @Software: PyCharm


from flask import request, g

from app.api import route_api
from app.models.admin.models import Admin
from common.libs.CustomException import ab_code_2
from common.libs.auth import check_user
from common.libs.tools import json_format


@route_api.before_request
def before_request_api():
    print('=== api_before_request ===')
    host = request.host
    print(host)
    method = request.method
    print(method)
    path = request.path
    print(path)
    print('=== headers ===')
    headers = {k: v for k, v in request.headers.items()}
    json_format(headers)
    print('=== params ===')
    json_format(request.args.to_dict())
    print('=== data ===')
    json_format(request.form.to_dict())
    print('=== json ===')
    json_format(request.get_json())

    w = ['/api/login']
    if path in w:
        return

    if '/api' in path:
        print('===访问 api==')
        is_token = request.headers.get('Token', None)  # 是否存在token
        print('头部是否存在key:token->', is_token)

        if is_token:
            token = request.headers.get('token', '')  # 提取token
            # print(token)
            # 通过token查找user
            # 将user存放在全局g对象中
            check_user(token=token, model=Admin)
        else:
            ab_code_2(666)

    else:
        g.app_user = None

# @route_api.after_request
# def after_request_cms(response):
#     pass

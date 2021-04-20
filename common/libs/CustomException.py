# -*- coding: utf-8 -*-
# @Time    : 2020/7/18 3:47 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : CustomException.py
# @Software: PyCharm


from werkzeug.exceptions import HTTPException

from flask import jsonify, abort, request
import flask_restful

# Common CustomException
EX_TEST = (333, '测试自定义异常')
Bad_Request = (400, '参数类型错误')
NOT_AUTHORIZED = (401, '未登录-认证信息失败-令牌过期')
FORBIDDEN = (403, '无权限')
ServerError = (500, '服务器内部异常')
NOT_TOKEN = (666, 'token呢？')
ICU = (996, '没救了')

# Api CustomException
OPERATING_ERROR = (100000, '异常操作')
PARAM_ERROR = (100005, '参数错误')
MODELS_ALREADY_EXISTS = (100006, '模型对象已经存在')
MODELS_NOT_FOUND = (100007, '模型对象不存在')

# CMS CustomException
CMS_ERROR = (999, 'cms gg')


class CustomException(HTTPException):
    code = None
    msg = None

    def __init__(self, code=None, msg=None):
        if code:
            self.code = code

        if msg:
            self.msg = msg
        super(CustomException, self).__init__(self.code, self.msg)


def ab_code(data):
    C = {

        400: Bad_Request,
        401: NOT_AUTHORIZED,
        403: FORBIDDEN,
        500: ServerError,
        666: NOT_TOKEN,
        333: EX_TEST
    }
    code = C.get(data)[0]
    print(code)
    msg = C.get(data)[1]
    print(msg)
    raise CustomException(code=code, msg=msg)


def ab_code_restful(data):
    """
    flask_restful 自定义异常
    """
    code = data[0]
    msg = data[1]
    req = request.method + ' ' + request.path
    r = {
        "code": code,
        "msg": msg,
        "request": req
    }
    return jsonify(r)


# 修改flask_restful.abort
def custom_abord(http_status_code, *args, **kwargs):
    if http_status_code == 400:
        abort(ab_code_restful(ICU))
    if http_status_code == 401:
        abort(ab_code_restful(NOT_AUTHORIZED))
    if http_status_code == 666:
        abort(ab_code_restful(NOT_TOKEN))
    if http_status_code == 100000:
        abort(ab_code_restful(OPERATING_ERROR))
    if http_status_code == 100005:
        abort(ab_code_restful(PARAM_ERROR))
    if http_status_code == 100006:
        abort(ab_code_restful(MODELS_ALREADY_EXISTS))
    if http_status_code == 100007:
        abort(ab_code_restful(MODELS_NOT_FOUND))
    return abort(http_status_code)


# 简化 flask_restful.abort
def ab_code_2(code):
    flask_restful.abort = custom_abord
    flask_restful.abort(code)

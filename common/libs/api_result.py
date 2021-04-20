# -*- coding: utf-8 -*-
# @Time    : 2020/7/18 3:45 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : api_result.py
# @Software: PyCharm

from flask import jsonify


# 返回格式
def api_result(code=None, message=None, data=None, details=None, status=None):
    result = {
        "code": code,
        "message": message,
        "data": data,
    }

    # if not result['data']:
    #     result.pop('data')
    #     return jsonify(result)
    return jsonify(result)

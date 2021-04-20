# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 下午7:53
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : conf_register.py
# @Software: PyCharm


from app.api import route_api


def register_bp(app):
    """蓝图注册"""

    """API蓝图注册"""
    app.register_blueprint(route_api, url_prefix="/api")

    """CMS蓝图注册"""
    pass

    """其他独立蓝图注册"""
    pass

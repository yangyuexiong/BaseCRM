# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 下午2:33
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : login.py
# @Software: PyCharm

from app.public_reference import *
from app.models.admin.models import Admin


class LoginApi(Resource):
    """
    登录
    """

    def get(self):
        return api_result(code=200, message='登录成功get')

    def post(self):
        data = request.get_json()
        # print(data)
        if check_keys(data, 'username', 'password'):
            username = data.get('username', '')
            password = data.get('password', '')
            user = Admin.query.filter_by(username=username).first()
            # print(user.__dir__())
            if user and user.check_password(password):
                # print(user.username)
                # print(user.password)
                """
                检查是否存在旧token并且生成新token覆盖旧token,或创建一个新的token。然后添加至返回值。
                """
                user_obj = user.to_json()
                user_obj['mobile'] = str(user.username)

                t = Token()
                t.check_token(user=user.username, user_id=user.id)
                user_obj['token'] = t.token
                return api_result(code=200, message='登录成功', data=user_obj)
            else:
                ab_code_2(200001)
        else:
            ab_code_2(100005)

    def delete(self):
        # print(request.headers.get('Token'))
        # del_token(request.headers.get('Token'))
        Token.del_token(request.headers.get('Token'))
        return api_result(code=204, message='退出成功')

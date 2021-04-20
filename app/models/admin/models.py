# -*- coding: utf-8 -*-
# @Time    : 2020/7/19 5:15 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : __init__.py.py
# @Software: PyCharm


from werkzeug.security import generate_password_hash, check_password_hash

from registry.db_register import db
from common.libs.BaseModel import BaseModel

crm_user_and_role = db.Table(
    'tp_user_and_role',
    db.Column('user_id', db.Integer, db.ForeignKey('tp_admin.id'), primary_key=True, comment='用户id'),
    db.Column('role_id', db.Integer, db.ForeignKey('tp_role.id'), primary_key=True, comment='角色id'),
    comment='用户_角色_中间表'
)

crm_permission_and_role = db.Table(
    'tp_permission_and_role',
    db.Column('permission_id', db.Integer, db.ForeignKey('tp_permission.id'), primary_key=True, comment='权限id'),
    db.Column('role_id', db.Integer, db.ForeignKey('tp_role.id'), primary_key=True, comment='角色id'),
    comment='权限_角色_中间表'
)


class Admin(BaseModel):
    __tablename__ = 'tp_admin'
    __table_args__ = {'comment': '用户表'}
    mobile = db.Column(db.String(255), nullable=True, comment='手机号')
    username = db.Column(db.String(255), nullable=False, comment='用户名')
    _password = db.Column(db.String(255), nullable=False, comment='密码')
    mail = db.Column(db.String(255), nullable=True, comment='邮箱')
    nickname = db.Column(db.String(255), nullable=True, comment='昵称')

    # 主键映射

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    def get_role(self):
        """获取当前用户的所有角色"""
        roles = self.roles
        # print(roles)
        roles_json = [r.to_json() for r in roles]
        return roles_json

    def get_permission(self):
        """获取当前用户的所有权限"""
        roles = self.roles
        permission_set = []
        for r in roles:
            permission_set += r.permission_list
        # print(list(set(permission_set)))
        permission_json = [p.to_json() for p in list(set(permission_set))]
        return permission_json

    def __repr__(self):
        return 'admin模型对象-> 用户名:{}'.format(self.username)


class Role(BaseModel):
    __tablename__ = 'tp_role'
    __table_args__ = {'comment': '后台角色表'}
    name = db.Column(db.String(50), nullable=False, comment='角色名称')
    remark = db.Column(db.String(255), nullable=True, comment='备注')

    user_list = db.relationship('Admin', secondary=crm_user_and_role, backref='roles')
    permission_list = db.relationship('Permission', secondary=crm_permission_and_role, backref='roles')

    def __repr__(self):
        return 'Role 模型对象-> ID:{} 角色名称:{}'.format(self.id, self.name)


class Permission(BaseModel):
    __tablename__ = 'tp_permission'
    __table_args__ = {'comment': '后台权限表'}
    name = db.Column(db.String(50), nullable=False, comment='权限名称')
    remark = db.Column(db.String(255), nullable=True, comment='备注')

    def __repr__(self):
        return 'Permission 模型对象-> ID:{} 权限名称:{}'.format(self.id, self.name)

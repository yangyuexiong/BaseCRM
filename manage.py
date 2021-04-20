# -*- coding: utf-8 -*-
# @Time    : 2020/7/18 4:02 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : manage.py
# @Software: PyCharm

import os

from flask_script import Manager, Server, Command
from flask_migrate import Migrate, MigrateCommand

from ApplicationExample import create_app
from registry.db_register import db
from app.public_reference import tp_db
from app.models.admin.models import Admin, Role, Permission

app = create_app()  # 实例
manager = Manager(app)  # 绑定
Migrate(app, db)
manager.add_command('db', MigrateCommand)  # 添加命令


# 自定义命令一：
class Hello(Command):
    """hello world"""

    def run(self):
        print('hello world')


class TableCreateFirst(Command):
    """首次映射并且创建表"""

    def run(self):
        try:
            os.system("python3 manage.py db init")
            os.system("python3 manage.py db migrate")
            os.system("python3 manage.py db upgrade")
            print('创建成功')
        except BaseException as e:
            print('创建失败:{}'.format(str(e)))


class TableCreate(Command):
    """增加表"""

    def run(self):
        try:
            os.system("python3 manage.py db migrate")
            os.system("python3 manage.py db upgrade")
            print('创建成功')
        except BaseException as e:
            print('创建失败:{}'.format(str(e)))


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_admin(username, password):
    """创建后台管理用户"""

    admin = Admin.query.filter_by(username=username).first()
    if admin:
        print('用户: {} 已存在'.format(admin))
    else:
        user = Admin(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        print('用户: {} 添加成功'.format(user))


# 添加命令
manager.add_command('hello', Hello())
manager.add_command('orm', TableCreateFirst())
manager.add_command('table', TableCreate())

# 自定义命令二：
# web server
manager.add_command(
    "runserver",
    Server(
        host='0.0.0.0',
        port=7777,
        use_debugger=True,
        use_reloader=True
    ))


def main():
    manager.run()


if __name__ == '__main__':
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()

    '''
    数据库
    在pipenv环境中在每个命令前加上 pipenv run
    如:pipenv run python3 manage.py 
    '''
    # 初始化迁移环境:python3 manage.py db init
    # 迁移数据库:python3 manage.py db migrate
    # 映射数据库:python3 manage.py db upgrade
    # 回滚:
    #   ps:先备份数据
    #       python3 manage.py db history
    #       python3 manage.py db downgrade id

    '''
    创建后台管理用户:
    pipenv run python3 manage.py create_admin -u yangyuexiong -p 123456 -m yuexiong.yang@happy-seed.com -n 杨跃雄 -r 1 -a 1
    '''

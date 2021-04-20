# -*- coding: utf-8 -*-
# @Time    : 2021/4/19 下午5:21
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : run.py
# @Software: PyCharm


import os
import warnings
# import platform
import threading

from common.libs.tools import get_host_ip
from ApplicationExample import create_app
from registry.hook_register import *  # 导入拦截器
from registry.excep_register import *  # 导入异常处理器

app = create_app()


def check_env(*args):
    """检查环境变量"""
    for i in args:
        if not os.environ.get(str(i)):
            # run_tips(str(i))
            msg = '\n\nTips:未找到Flask环境变量 "FLASK_ENV" 请配置!如需了解配置可查阅:https://github.com/yangyuexiong/Flask_BestPractices\n\n'
            exit(msg)


def main():
    """启动"""

    check_env('FLASK_ENV')  # 必须变量

    if platform.system() == 'Linux':
        app.run(host=app.config['RUN_HOST'], port=app.config['RUN_PORT'])

    else:
        app.run(debug=app.config.get('DEBUG'), host=app.config.get('RUN_HOST'), port=app.config.get('RUN_PORT'))
        # app.run(debug=app.config.get('DEBUG'), host='192.168.110.58', port=9999)


if __name__ == '__main__':
    pass
    """
    # 设置环境
    export FLASK_ENV=development
    export FLASK_ENV=production
    
    export STARTUP_MODE=pyc
    export STARTUP_MODE=ter
    
    # 调试
    os.environ.get('FLASK_ENV')
    os.environ.get('STARTUP_MODE')
    """

    flask_env = os.environ.get('FLASK_ENV')
    startup_mode = os.environ.get('STARTUP_MODE')
    print('<', '-' * 66, '>')
    print('时间:{}'.format(datetime.datetime.now()))
    print('IP:{}'.format(get_host_ip()))
    print('操作系统:{}'.format(platform.system()))
    print('项目路径:{}'.format(os.getcwd()))
    print('当前环境:{}'.format(flask_env))
    print('启动方式:{}'.format(startup_mode))
    print('threading:{}'.format(threading.get_ident()))
    print('当前进程id:{}'.format(os.getpid()))
    print('父进程id:{}'.format(os.getppid()))
    print('DEBUG:{}'.format(app.config.get('DEBUG')))
    print('<', '-' * 66, '>')
    main()

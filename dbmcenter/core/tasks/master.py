# -*- coding: utf8 -*-

"""
dbm-center 可能会被运行在多台机器的多个进程上，虽然大家都可以处理 http 请求，但是对于关键状态应该只有一个进程可以读写。

"""

import time
import random
import logging

from dbmcenter.settings import IS_MASTER_ROLE_ENABLED
from dbmcenter.core.tasks.base import DbmBaseTask, threads, init_task_framework, submit_backend_task


logger = logging.getLogger('dbmcenter.core.tasks')


class RegisterMasterTask(DbmBaseTask):
    """
    注册 dbm-master 结点信息
    """

    def register_master(self):
        """
        把自己注册为 master
        """
        # 对于 swgi 这种多进程的场景，这里随机一下不要让它们同时去抢主
        time.sleep(random.randint(3, 29))

        # 抢到主的进程不断的序约，没有抢到的进程也不会放
        # 序约 13 秒一次
        # 抢主 27 秒一次
        while True:
            logger.info("register-master:")
            # TODO
            time.sleep(13)

    def __call__(self):
        self.register_master()


def init_master():
    """
    初始化 master 角色
    """
    # 如果不启动 MASTER 状态就直接退出
    if not IS_MASTER_ROLE_ENABLED:
        return
    
    global threads
    if threads is None:
        # 激活异步任务框架
        init_task_framework()
        submit_backend_task(RegisterMasterTask())

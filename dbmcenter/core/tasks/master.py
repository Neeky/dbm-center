"""
对于 dbm-center 来说一个 http 请求对应的操作可能会非常的长，比如安装一套高可用的 MySQL 集群；如果等这一切都执行完成之后再返回 JsonResponse 的话，浏览器就会超时。

为了尽可能快的返回给客户端，dbm-center 在做完成必要的检查，并且把任务的信息保存到后端 MySQL 后就返回给客户端。
"""

import time
import random
import logging

from dbmcenter.core.tasks.base import DbmBaseTask, threads, init_task_framework, submit_backend_task


logger = logging.getLogger('dbmcenter.core.tasks')


class DbmCenterMasterTask(DbmBaseTask):
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
    global threads
    if threads is None:
        # 激活异步任务框架
        init_task_framework()
        submit_backend_task(DbmCenterMasterTask())

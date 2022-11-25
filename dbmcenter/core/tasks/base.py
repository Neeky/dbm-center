# -*- coding: utf8 -*-
"""
基于 concurrent.futures.thread.ThreadPoolExecutor 实现一个异步任务框架，对于长时间的任务直接交结异步构架执行，以便尽快的返回 JsonResponse 。

这里的实现参考了 JavaScript 的并发模型 "https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/EventLoop"

"""


import logging
from uuid import uuid4
from concurrent.futures.thread import ThreadPoolExecutor

from dbmcenter.settings import BACKEND_THREAD_POOL_SIZE

threads = None

logger = logging.getLogger('dbmcenter.core.task')


class DbmBaseTask(object):
    """
    所有 dbm-center task 的基类
    """

    def __init__(self):
        """
        """
        self.task_id = uuid4()

    def check(self):
        """
        检查任务能否执行
        """
        raise NotImplementedError("DbmBaseTask.check NotImplemented")

    def save(self):
        """
        如果任务在 MySQL 中不存在，就接入
        如果任务在 MySQL 中已存在，就更新
        """
        raise NotImplementedError("DbmBaseTask.save NotImplemented")
    
    def __call__(self):
        """
        每个任务都是一个可以执行的对象
        """
        raise NotImplementedError("DbmBaseTask.__call__ NotImplemented")



def execute_task(task):
    """
    """
    logging.info(f"backend threads pool size = {BACKEND_THREAD_POOL_SIZE} .")
    try:
        task()
    except Exception as err:
        logger.error("execute task fail.")
        logger.error(str(err))


def submit_backend_task(task:DbmBaseTask):
    """
    添加后台执行任务
    """
    threads.submit(execute_task, task)


def init_task_framework():
    """
    初始化后台执行框架
    """
    global threads
    if threads is None:
        threads = ThreadPoolExecutor(max_workers=BACKEND_THREAD_POOL_SIZE)

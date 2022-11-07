# -*- coding: utf8 -*-

import json
import logging

from django.utils import timezone
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.generic.base import View

from agents.models import Agent
from dbmcenter.consts import APPLICATION_JSON

logger = logging.getLogger('agents')


class AgentsView(View):
    """
    所有 agent 对象 crud 的接口
    """

    def get(self, request, *args, **kwargs):
        """
        查询出所有已经注册的 Agent 信息，并返回


        Parameters
        ----------
        request : WSGIRequest
            请求对象

        args: tuple
            位置参数、默认 ()

        kwargs: disct
            关键字参数、默认 {}


        Returns
        -------
        result : JsonReponse
            返回所有 agent 的列表
        """
        logger.info(
            f"path = {request.path} method= {request.method} args = {args}  kwargs = {kwargs} .")
        result = []
        message = ''
        try:
            result = [_ for _ in Agent.objects.values()]
        except Exception as err:
            message = f"query all agents got fail, inner error = {str(err)}"
            logger.error(message)

        return JsonResponse({
                'agents': result,
                'message': message
            })

    def post(self, request, *args, **kwargs):
        """
        agent 首次注册的时候会调用这个 post 方法

        Parameters
        ----------
        request : WSGIRequest
            请求对象

        args: tuple
            位置参数、默认 ()

        kwargs: disct
            关键字参数、默认 {}
        """
        # 检查 header
        logger.info(
            f"path = {request.path} method= {request.method} args = {args}  kwargs = {kwargs} .")
        if request.headers["Content-Type"] != APPLICATION_JSON:
            logger.warning(
                f"request.headers['Content-Type'] != '{APPLICATION_JSON}', we well reject it .")
            return JsonResponse({
                'message': 'pelease use application/json post your data.'
            })

        # 提取数据
        logger.info(f"start translate playload to json .")
        data = json.loads(request.body.decode('utf8'))
        logger.info(f"data = {data} .")

        # 业务逻辑的检查
        host = data.get('host', '')
        port = data.get('port', 8086)
        version = data.get('version', '0.0.0')
        now = timezone.now()
        if host == '':
            return JsonResponse({
                'message': 'host is empty , not valide .'
            })
        logger.info(f"host = {host} port = {port} version = {version} .")

        # 写回到数据库
        try:
            agent = Agent.objects.create(host=host, port=port, version=version, register_at=now, heartbeat_at=now)
        except IntegrityError as err:
            # 由于  host 要保证唯一，当提交上来的 host 已经存在的时候就会引发完整性约束异常
            logger.warning(f"looks like host = {host} , has been exists.")
            return JsonResponse({
                'message': str(err)
            })
        except Exception as err:
            logger.warning(type(err))
            return JsonResponse({
                'message': str(err)
            })
        
        # 返回 agent 的 id 值到 client
        return JsonResponse({
                'id': agent.pk,
                'message': '',
            })

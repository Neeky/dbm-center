# -*- coding: utf8 -*-

import json
import logging

from django.utils import timezone
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.generic.base import View
from django.forms.models import model_to_dict

from agents.models import Agent
from dbmcenter.consts import APPLICATION_JSON

logger = logging.getLogger('agents')


class AgentsView(View):
    """
    所有 agent 对象 crud 的接口
    """

    def get(self, request, agent_pk='', *args, **kwargs):
        """
        根据 agent_pk 查询出对应的 agent 信息并返回，如果 agent_pk = '' 就返回所有的 agent 对象。

        Parameters
        ----------
        request : WSGIRequest
            请求对象

        agent_pk: str
            接口传进来的 agent 的主键，由于项目使用的 re 来匹配参数，所以在接口没有传入参数时会得到空值

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
            f"path = {request.path} method= {request.method} agent-pk = '{agent_pk}' args = {args}  kwargs = {kwargs} .")
        result = []
        message = ''

        # 处理有传入主键的情况
        if agent_pk != '':
            logger.info(f"query one agent by pk = {agent_pk}.")
            pk = int(agent_pk)

            try:
                agent = Agent.objects.get(pk=pk)
                return JsonResponse(model_to_dict(agent))
            except Agent.DoesNotExist as err:
                # Agent matching query does not exist.
                logger.warning(str(err))
                return JsonResponse({
                    'message': str(err)
                })

        # 处理查询所有的情况
        try:
            logger.info(f"query all agents .")
            result = [_ for _ in Agent.objects.values()]
            return JsonResponse({
                'agents': result,
                'message': message
            })

        except Exception as err:
            message = f"query all agents got fail, inner error = {str(err)}"
            logger.error(message)

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
            agent = Agent.objects.create(
                host=host, port=port, version=version, register_at=now, heartbeat_at=now)
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

    def put(self, request, agent_pk, *args, **kwargs): 
        """
        更新 agent 的心跳信息

        Parameter
        ---------
        agent_pk: int
            agent 的主键

        Return:
        ------
        {
            'pk': agent.pk,
            'message':''
        }
        """
        logger.info(f"{request} {agent_pk} {args} {kwargs}")

        if agent_pk != '':
            pk = int(agent_pk)
        else:
            return JsonResponse({
                'message': 'agent-pk should be int .'
            })

        # 更新 heartbeat
        try:
            agent = Agent.objects.get(pk=pk)
            agent.update_heartbeat()
        except Agent.DoesNotExist as err:
            return JsonResponse({
                'message': str(err)
            })
        # 
        return JsonResponse({
            'pk': agent.pk,
            'message': ''
            })

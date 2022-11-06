# -*- coding: utf8 -*-

import logging
from datetime import datetime

from django.http import JsonResponse
from django.views.generic.base import View

from agents.models import Agent

logger = logging.getLogger(__name__)

class AgentsView(View):
    """
    所有 agent 对象 crud 的接口
    """

    def get(self, request, *args, **kwargs):
        """
        """
        logger.info(f"request = {request} args = {args}  kwargs = {kwargs}")
        return JsonResponse(
            {
                'agents':[_ for _ in Agent.objects.values()],
                'message': ''
            }
        )

    def post(self, request, *args, **kwargs):
        """
        """
        logger.error(f"request = {request.POST} args = {args}  kwargs = {kwargs}")
        logger.error(f"request.post = {dir(request)} args = {args}  kwargs = {kwargs}")
        agent = Agent.objects.create(host = '127.0.0.2', version = '0.0.1', register_at = datetime.now(), port = 8086, heartbeat_at = datetime.now())
        agent.save()
        return JsonResponse(
            {
                'message': 'ok'
            }
        )



def all_agents(request, *args, **kwargs):
    return JsonResponse({
        'agents': [],
        'message': ''
    })

# -*- coding: utf8 -*-

"""
返回 dbm-center 的配置信息方便查询
"""
import os
import logging
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic.base import View
from dbmcenter import settings

logger = logging.getLogger('dbmcenter.views.configs')

class DBMCenterConfigView(View):
    """返回 DBMCenter 的配置信息
    """
    def get(self, request,  *args, **kwargs):
        """读取 settings.py 中的部分配置返回给客户端
        """
        logger.info(f"path = {request.path} method= {request.method} args = {args}  kwargs = {kwargs} .")

        # 读取配置
        basedir = str(settings.BASE_DIR)
        engine = settings.DATABASES['default']['ENGINE']
        name = ''
        if engine == 'django.db.backends.sqlite3':
            name = os.path.join(basedir, 'dbmcenter.sqlite3')
        
        # 返回结果
        return JsonResponse(data={
            'BASE_DIR': basedir,
            'ENGINE': engine,
            'NAME': name,
            'CURRENT': timezone.now()
        })
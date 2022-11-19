from django.db import models
from django.utils import timezone

import logging
# Create your models here.

logger = logging.getLogger("agents")

class Agent(models.Model):
    """
    用于保留系统里面每一个 Agent 的信息
    """

    # 心跳上报的超时时间
    HEARTBEAT_EXPIRE_TIME_SECONDES = 11

    # agent 所在主机的地址/域名
    host = models.GenericIPAddressField(unique=True, default='127.0.0.1')

    # agent 的版本号
    version = models.CharField(max_length=16)

    # 端口
    port = models.IntegerField(default=8086)

    # 注册到系统的时间
    register_at = models.DateTimeField(default=timezone.now)

    # 最近一次上报心跳的时间点
    heartbeat_at = models.DateTimeField(default=timezone.now)

    @property
    def is_alive(self):
        """
        heartbeat_at 用于保存 agent 上报心跳时的时间点，is_alive 去检查这个时间点，如果这个时间点距离当前时间点小于 11s 就算活着的。
        """
        now = timezone.now()
        logger.debug(f"check agent is alive , now = {now} agent.heartbeat_at = {self.heartbeat_at} .")
        if (now - self.heartbeat_at) > timezone.timedelta(seconds=self.HEARTBEAT_EXPIRE_TIME_SECONDES):
            logger.warning(f"agent is not alive (now - self.heartbeat_at) = {now - self.heartbeat_at}. ")
            return False

        return True 

    @property
    def is_connectble(self):
        """
        dbm-center 能否连接到 dbm-agent,
        """
        return False

    def update_heartbeat(self):
        """
        更新 agent 的心跳信息
        """
        self.heartbeat_at = timezone.now()
        self.save()

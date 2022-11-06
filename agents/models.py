from django.db import models

# Create your models here.

class Agent(models.Model):
    """
    用于保留系统里面每一个 Agent 的信息
    """
    # agent 所在主机的地址/域名
    host = models.GenericIPAddressField()

    # agent 的版本号
    version = models.CharField(max_length=16)

    # 注册到系统的时间
    register_at = models.DateTimeField()

    # 端口
    port = models.IntegerField(default=8086)

    # 最近一次上报心跳的时间点
    heartbeat_at = models.DateTimeField()
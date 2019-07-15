import uuid
from django.db import models
from . import idc

class HostType(models.Model):
    """
    保存机型信息
    """
    band_width = [('1G','1G'),('10G','10G')]

    name = models.CharField(max_length=32,help_text="机型名称")
    oem_name = models.CharField(max_length=64,help_text="首家名称")
    cpu_cores = models.PositiveSmallIntegerField(help_text="cpu 逻辑核心数量")
    mem_bytes = models.BigIntegerField(help_text="内存大小(byte)")
    eth_bands = models.CharField(max_length=16,choices=band_width,help_text="网卡带宽")
    disk_size = models.BigIntegerField(help_text="磁盘容量(bytes)")

    class Meta:
        unique_together = [['name', 'oem_name','cpu_cores','mem_bytes','eth_bands']]

class Host(models.Model):
    """
    保存主机信息
    """
    ip = models.GenericIPAddressField(help_text="主机的ip地址") # 目前只支持一个IP的情况，还不支持多个IP，可以把这个IP设置成管理网的IP
    hostname = models.CharField(max_length=128,help_text="主机IP经过DNS解析后的名称",default="localhost")
    hostuuid = models.UUIDField(verbose_name="主机唯一标识",default=uuid.uuid4)
    hosttype = models.ForeignKey(HostType,verbose_name="主机类型",on_delete=models.CASCADE,default=1)
    idc = models.ForeignKey(idc.IDC,verbose_name="主机所在的IDC机房",on_delete=models.CASCADE,default=1)
    



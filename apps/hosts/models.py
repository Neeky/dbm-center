from django.db import models
from django.core import exceptions
# Create your models here.


class HostManager(models.Manager):
    """
    """
    def get_host_id_by_uuid(self,host_uuid:str=""):
        try:
            h = super().get(host_uuid=host_uuid)
        except exceptions.ValidationError:
            return None
        except HostModel.DoesNotExist:
            return None
        except Exception:
            return None
        return h.id

class HostModel(models.Model):
    """
    用于保存主机层面的常用信息
    """
    host_uuid = models.UUIDField("主机标识",unique=True)
    agent_version = models.CharField("dbm-agent 版本号",max_length=16,default='',help_text="dbm-agent 版本号")
    cpu_cores = models.PositiveIntegerField('CPU 逻辑核心数量',default=0,help_text="CPU 逻辑核心数量")
    mem_total_size = models.PositiveIntegerField('物理内存大小',default=0,help_text="物理内存大小(字节)")
    create_time = models.DateTimeField("主机添加 dbmc 的时间",auto_now_add=True)
    modify_time = models.DateTimeField("最近一次修改的时间",auto_now=True)
    manger_net_ip = models.GenericIPAddressField("管理网 IP 地址")
    os_version = models.CharField("操作系统版本号",max_length=32,default='',help_text="dbm-agent 版本号")
    objects = models.Manager()
    hosts = HostManager()

    def __str__(self):
        return f"HostModel({self.manger_net_ip})"


# 网卡
class NetInterfaceModel(models.Model):
    """
    网络接口信息，主机上的每一个网卡(除 lo 之外)，都应该在这个表中有一行与之对应
    """
    # 当主机被删除之后网卡也不应该存在了
    host = models.ForeignKey(HostModel,on_delete=models.CASCADE)
    name = models.CharField('网上的名字',max_length=16)
    speed = models.PositiveIntegerField('网卡的带宽')
    isup = models.BooleanField('网卡的状态')
    address = models.GenericIPAddressField('网卡地址')
    create_time = models.DateTimeField("添加时间",auto_now_add=True)
    modify_time = models.DateTimeField("最近一次修改的时间",auto_now=True)

    def __str__(self):
        return f"{self.address}:{self.name}"

class NetIOCounterModel(models.Model):
    """
    主机级别的网络IO收发情况
    """
    host = models.ForeignKey(HostModel,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    bytes_sent = models.BigIntegerField('发送的总字节数')
    bytes_recv = models.BigIntegerField('接收的总字节数')
    sent_perm = models.DecimalField('每分钟发送字节的速度',max_digits=16,decimal_places=3)
    recv_perm = models.DecimalField('每分钟接收字节的速度',max_digits=16,decimal_places=3)


# cpu
class CpuTimesModel(models.Model):
    """
    cpu 时间片分布监控
    """
    host = models.ForeignKey(HostModel,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.DecimalField("cpu user",max_digits=5,decimal_places=3)
    system = models.DecimalField("cpu system",max_digits=5,decimal_places=3)
    idle   = models.DecimalField("cpu idle",max_digits=5,decimal_places=3)
    nice = models.DecimalField("cpu nice",max_digits=5,decimal_places=3)
    iowait = models.DecimalField("cpu iowait",max_digits=5,decimal_places=3)
    irq = models.DecimalField("cpu irq",max_digits=5,decimal_places=3)
    softirq = models.DecimalField("cpu softirq",max_digits=5,decimal_places=3)

class CpuFrequencyModel(models.Model):
    """
    cpu 运行频率监控
    """
    host = models.ForeignKey(HostModel,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    current = models.PositiveIntegerField("当前运行频率")

# 内存
class MemoryDistriModel(models.Model):
    """
    内存使用情况监控
    """
    host = models.ForeignKey(HostModel,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField('内存总大小')
    available = models.PositiveIntegerField('内存可用空间大小')
    used = models.PositiveIntegerField('内存已经使用部分的大小')
    free = models.PositiveIntegerField('内存空闲使用部分的大小')


class DiskUsageModel(models.Model):
    """
    磁盘使用率监控
    """
    host = models.ForeignKey(HostModel,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    mount_point = models.CharField('挂载点',max_length=64)
    total = models.BigIntegerField('总大小')
    used = models.BigIntegerField('已经使用空间的大小')
    free = models.BigIntegerField('空间空间的大小')


class DiskIOCounterModel(models.Model):
    """
    主机级别的磁盘IO读写情况
    """
    host = models.ForeignKey(HostModel,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    read_count = models.BigIntegerField(default=0)
    write_count = models.BigIntegerField(default=0)
    read_bytes = models.BigIntegerField(default=0)
    write_bytes = models.BigIntegerField(default=0)
    read_cps = models.DecimalField('每秒读操作的次数',default='0',max_digits=12,decimal_places=3)
    write_cps = models.DecimalField('每秒写操作的次数',default='0',max_digits=12,decimal_places=3)
    read_kps = models.DecimalField('每秒的读速度kps',default='0',max_digits=12,decimal_places=3)
    write_kps = models.DecimalField('每秒的写速度kps',default='0',max_digits=12,decimal_places=3)





    

    
    
    

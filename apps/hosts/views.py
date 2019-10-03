import logging
from django.views import View
from django.shortcuts import render
from django.utils.timezone import now,timedelta
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


from . import models
from . import forms


logger = logging.getLogger('dbmc').getChild('apps.hosts.views')

class HostsView(View):
    """
    实现对主机信息的上传与查询
    """
    logger = logger.getChild("HostView")

    @method_decorator(ensure_csrf_cookie)
    def get(self,request):
        """
        查询指定的 HostModel 或查询所有的 HostModel
        """
        self.logger.info(f"HostsView.get function dbmc will return an host info or return all host info")
        self.logger.debug(f"HostsView.get request.GET = {request.GET}")

        if request.GET == {} :
            # request.GET 有重载 __eq__ 所以支持与空字典的比较
            self.logger.info("return all host info")
            hosts = models.HostModel.objects.all().values("host_uuid","agent_version","cpu_cores","mem_total_size","manger_net_ip","os_version")
            result = {
                'code': 200,
                'message': '所有的 host 信息',
                'data': [dict(host) for host in hosts]
            }
            self.logger.info(f"result = {result}")
            return JsonResponse(result)
        else:
            try:
                if 'pk' in request.GET:            # 支持 pk 查询
                    hm = models.HostModel.objects.get(pk=request.GET.get('pk'))
                elif 'host_uuid' in request.GET:   # 支持 uuid 查询
                    hm = models.HostModel.objects.get(host_uuid=request.GET.get('host_uuid'))
                
                host = {'host_uuid': hm.host_uuid,
                        'agent_version': hm.agent_version,
                        'cpu_cores': hm.cpu_cores,
                        'mem_total_size': hm.mem_total_size,
                        'manger_net_ip': hm.manger_net_ip}

                result = {
                        'code': 201,
                        'message': '没有满足条件的内容',
                        'data': [host]
                    }
                return JsonResponse(result)
            
            except models.HostModel.DoesNotExist:
                # 由于 pk host_uuid 都是唯一的，所以不会存在一值多行的情况
                    result = {
                        'code': 400,
                        'message': '没有满足条件的内容',
                        'data': []
                    }
            
            return JsonResponse(result)
    
    
    @method_decorator(ensure_csrf_cookie)
    def post(self,request):
        """
        添加或更新 HostModel
        """
        self.logger.info("post function dbmc will insert or update a host info")
        self.logger.debug(f"post function request.POST = {request.POST}")
        host = forms.HostForm(request.POST)
        if host.is_valid():
            host.save()
            # 添加时的返回结果
            result = {
                'code': 200,
                'message': "数据库中还没有这条记录已经插入成功"
            }
            self.logger.info(f"insert an host info record.")

            return JsonResponse(result)

        else:
            if 'host_uuid' not in host.cleaned_data :
                # 说明 host_uuid 对应的行都已经在数据库存在了，这样只要更新
                host_uuid = request.POST.get('host_uuid')
                logger.info(host_uuid)
                try:
                    hm = models.HostModel.objects.get(host_uuid=host_uuid)
                    hm.mem_total_size = host.cleaned_data['mem_total_size']
                    hm.cpu_cores = host.cleaned_data['cpu_cores']
                    hm.agent_version = host.cleaned_data['agent_version']
                    hm.manger_net_ip = host.cleaned_data['manger_net_ip']
                    hm.os_version = host.cleaned_data['os_version']
                    #hm.update(host.cleaned_data)
                    hm.save()
                                    # 更新时的返回结果
                    result = {
                        'code': 201,
                        'message': f'数据库中已经存在 host_uuid = {host_uuid} ,服务端已经完成了对这条记录的更新'
                    }
                    self.logger.info(f"update an host info record.")
                    return JsonResponse(result)

                except models.HostModel.DoesNotExist:
                    pass

        # 定义一个保底逻辑
        result = {
            'code': 500,
            'message': '触发了未知的逻辑',
            'data': []
        }
        return JsonResponse(result)


class CpuTimesView(View):
    """
    """
    logger = logger.getChild("CpuTimesView")

    @method_decorator(ensure_csrf_cookie)
    def get(self,request,host_uuid=None):
        """
        按需查询时间片分布
        1、pk 
        1、latest 查询指定主机最新的那一条记录
        """
        if 'pk' in request.GET:
            pk = request.GET.get('pk')
            try:
                ct = models.CpuTimesModel.objects.get(pk = pk,host__host_uuid=host_uuid)
                result = {
                    'code': 200,
                    'message': f'查询到对应的数据',
                    'data': [{'user': ct.user,
                              'system': ct.system,
                              'idle': ct.idle,
                              'nice': ct.nice,
                              'iowait': ct.iowait,
                              'irq': ct.irq,
                              'softirq': ct.softirq,
                              'create_time': ct.create_time}]
                }
                return JsonResponse(result)
            except models.CpuTimesModel.DoesNotExist as err:
                result = {
                    'code': 201,
                    'message': "没有找到对应的数据行",
                }
                return JsonResponse(result)
        elif 'latest' in request.GET:
            try:
                ct = models.CpuTimesModel.objects.latest(host_uuid=host_uuid)
                result = {
                    'code': 200,
                    'message': f'查询到对应的数据',
                    'data': [{'user': ct.user,
                              'system': ct.system,
                              'idle': ct.idle,
                              'nice': ct.nice,
                              'iowait': ct.iowait,
                              'irq': ct.irq,
                              'softirq': ct.softirq,
                              'create_time': ct.create_time}]
                }
                return JsonResponse(result)
            except Exception as err:
                result = {
                    'code':202,
                    'message': f"没有找到对应的数据行"
                }
        else:
            # 返回当前主机最近 15 天的数据
            current_time = now() - timedelta(days=15)
            cts = models.CpuTimesModel.objects.filter(create_time__gt=current_time).values(
                "user",
                "system",
                "idle",
                "nice",
                "iowait",
                "irq",
                "softirq",
                "create_time")
            result = {
                'code': 200,
                'message': '最近 15 天 cpu 时间版本的分布情况',
                'data': [dict(ct) for ct in cts ]
            }
            return JsonResponse(result)


    @method_decorator(ensure_csrf_cookie)
    def post(self,request,host_uuid=None):
        """
        保存 cpu 时间片信息
        # 第一步：查询父表看对应的 host 信息是不是存在
        """

        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)
        if host_id == None:
            result = {
                'code': 400,
                'message': f"{host_uuid} 对应的主机信息不存在，无法添加 cpu 时间片监控",
                'data': []
            }
            return JsonResponse(result)

        try:
            user = float(request.POST.get('user'))
            system = float(request.POST.get('system'))
            idle = float(request.POST.get('idle'))
            nice = float(request.POST.get('nice'))
            iowait = float(request.POST.get('iowait'))
            irq = float(request.POST.get('irq'))
            softirq = float(request.POST.get('softirq'))
        except ValueError as err:
            result = {
                'code': 500,
                'message': '数据不能够正常的转换成浮点数',
                'data':[request.POST.dict()]
            }
            return JsonResponse(result)

        ct = models.CpuTimesModel(host_id=host_id,
                                  user=user,
                                  system=system,
                                  idle=idle,
                                  nice=nice,
                                  iowait=iowait,
                                  irq=irq,
                                  softirq=softirq)
        ct.save()

        result = {
            'code': 200,
            'message': "保存成功",
            'data': []
        }
        return JsonResponse(result)


class CpuFrequenceView(View):
    """
    """
    logger = logger.getChild('CpuFrequenceView')

    @method_decorator(ensure_csrf_cookie)
    def get(self,request,host_uuid):
        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)
        if host_id != None:
            # 说明对应的主机存在，就有可能有数据
            if 'pk' in request.GET:
                # 通过主键查询
                try:
                    cf = models.CpuFrequencyModel.objects.filter(host_id=host_id).order_by('create_time').last()
                    if cf == None:
                        result = {
                            'code': 400,
                            'message': "找不到对应的数据",
                            'data': []
                        }
                        return JsonResponse(result)
                    else:
                        result = {
                            'code': 200,
                            'message': '',
                            'data': [{
                                'current':cf.current
                            }]
                        }
                        return JsonResponse(result)
                except models.CpuFrequencyModel.DoesNotExist:
                    result = {
                        'code': 400,
                        'message': '找不到对应的数据',
                        'data': []
                    }
                    return JsonResponse(result)
            else:
                # 返回最近 15 天的数据
                current_time = now() - timedelta(days=15)
                cfs = models.CpuFrequencyModel.objects.filter(create_time__gt=current_time).values("create_time","current")
                result = {
                    'code': 200,
                    'message': "最近 15 天的数据",
                    'data': [cf for cf in cfs]
                }
                return JsonResponse(result)
        else:
            result = {
                'code': 400,
                'message': '没有找到对应的主机信息，无法保存 cpu 当前的运行频率',
                'data': []
            }
            return JsonResponse(result)

    @method_decorator(ensure_csrf_cookie)
    def post(self,request,host_uuid):
        """
        """
        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)

        if host_id != None:
            try:
                current = int(float(request.POST.get('current')))
                cf = models.CpuFrequencyModel(current=current,host_id=host_id)
                cf.save()
                result = {
                    'code': 200,
                    'message': "保存成功",
                    'data': []
                }
                return JsonResponse(result)
            except ValueError as err:
                print(err)
                result = {
                    'code': 500,
                    'message': '数据类型转换时遇到了错误',
                    'data': []
                }
                return JsonResponse(result)
            
            result = {
                'code': 501,
                'message': '触发了未知的异常',
                'data': []
            }
            return JsonResponse(result)
        else:
            result = {
                'code': 400,
                'messsage': "没有对应的 host 信息不能保存 cpu 运行时的主频信息",
                'data': []
            }
            return JsonResponse(result)


class NetInterfaceView(View):
    """
    实现对网卡信息的上传与查询
    """
    logger = logger.getChild("NetInterfaceView")

    @method_decorator(ensure_csrf_cookie)
    def get(self,request,host_uuid=""):
        """
        """
        try:
            nifs = models.NetInterfaceModel.objects.filter(host__host_uuid=host_uuid).values("name",
                    "speed","isup","address")
            
            result = {
                'code': 200,
                'message': '',
                'data': [nif for nif in nifs]
            }
            return JsonResponse(result)
        except Exception as err:
            self.logger.info(str(err))
        
        result = {
            'code': 500,
            'message': '触发了未知的逻辑',
            'data': []
        }
        return JsonResponse(result)

    @method_decorator(ensure_csrf_cookie)
    def post(self,request,host_uuid=None):
        """
        """
        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)
        if host_id == None:
            result = {
                'code': 400,
                'message': f'找不到 host_uuid = {host_uuid} 对应的主机，无法进行一下步网卡信息上传的逻辑',
                'data': []
            }
            return JsonResponse(result)
        
        try:
            name = request.POST.get('name')
            speed = int(request.POST.get('speed'))
            isup = bool(request.POST.get('isup'))
            address = request.POST.get('address')
            # 如果对应的网卡信息已经存在就进入更新逻辑
            nif = models.NetInterfaceModel.objects.get(host__host_uuid=host_uuid,name=name)
            nif.speed = speed
            nif.isup = isup
            nif.address = address
            nif.save()
            result = {
                'code': 200,
                'message': '数据库中存在对应的网卡信息，更新成功',
                'data': []
            }
            return JsonResponse(result)

        except ValueError as err:
            self.logger.info(f"convert fail {request.POST}")
            result = {
                'code': 500,
                'message': '在进入数据类型转换时失败',
                'data': [request.POST.dict()]
            }
            return JsonResponse(result)

        except models.NetInterfaceModel.DoesNotExist:
            nif = models.NetInterfaceModel(host_id=host_id,name=name,speed=speed,isup=isup,address=address)
            nif.save()

            result = {
                'code': 200,
                'message': '成功',
                'data': []
            }
            return JsonResponse(result)
        
        result = {
            'code': 501,
            'message': '触发了未知的异常',
            'data': []
        }
        return JsonResponse(result)
        

class NetIOCounterView(View):
    """
    实现网络 IO 计数器相关的监控
    """
    logger = logger.getChild("NetIOCounterView")
    @method_decorator(ensure_csrf_cookie)
    def get(self,request,host_uuid):
        """
        查询网络 IO 监控
        """
        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)

        if host_id == None:
            result = {
                'code': 400,
                'message': "找不到对应的主机信息，所以没难返回网络 IO 监控项",
                'data': []
            }
            return JsonResponse(result)
        else:
            # 说明监控项存在
            if 'pk' in request.GET:
                pk = request.GET.get('pk')
                try:
                    nic = models.NetIOCounterModel.objects.get(pk=pk)
                    result = {
                        'code': 200,
                        'message': "数据查询成功",
                        'data': [{
                            'create_time': nic.create_time,
                            'bytes_sent': nic.bytes_sent,
                            'bytes_recv': nic.bytes_recv,
                            'sent_perm': nic.sent_perm,
                            'recv_perm': nic.recv_perm,
                        }]
                    }
                    return JsonResponse(result)
                except models.NetIOCounterModel.DoesNotExist:
                    self.logger.info(f"没能找到 pk = {pk} 对应的 NetIOCounter 对象")
                    result = {
                        'code': 501,
                        'message': '没能找到对应的数据',
                        'data':[]
                    }
                    return JsonResponse(result)
            else:
                # 返回最近 15 天的数据
                current_time = now() - timedelta(days=15)
                nics = models.NetIOCounterModel.objects.filter(host_id=host_id,create_time__gt=current_time).values(
                    'create_time',
                    'bytes_sent',
                    'bytes_recv',
                    'sent_perm',
                    'recv_perm')

                result = {
                    'code': 200,
                    'message': "最近 15 天的数据",
                    'data': [nic for nic in nics]}
                
                return JsonResponse(result)

    @method_decorator(ensure_csrf_cookie)
    def post(self,request,host_uuid):
        """
        录入 网络 IO 监控 
        """
        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)

        if host_id == None:
            result = {
                'code': 400,
                'message': '无法查询到对应的主机信息，没有办法录入网络 IO 监控数据',
                'data':[]
            }
            return JsonResponse(result)
        else:
            # 1、说明对应的主机是存在的，那就可以录入主机对应的监控了
            try:
                # 对上报上来的数据进行类型转换
                bytes_sent = int(request.POST.get('bytes_sent'))
                bytes_recv = int(request.POST.get("bytes_recv"))
            except ValueError:
                result = {
                    'code': '500',
                    'message': '在对上报上来的数据进入类型转换时遇到了错误',
                    'data': []
                }
                return JsonResponse(result)

            nio_latest = models.NetIOCounterModel.objects.filter(host_id=host_id).order_by('create_time').last()

            if nio_latest == None:
                # 空结果，说明数据库里面还没有数据，那么当前要插入的数据就是第一条数据
                nio = models.NetIOCounterModel(bytes_sent=bytes_sent,
                                               bytes_recv=bytes_recv,
                                               sent_perm=0,
                                               recv_perm=0,
                                               host_id=host_id)
                nio.save()
                result = {
                    'code': 200,
                    'message': '网络监控的第一条数据插入成功',
                    'data': []
                }
                return JsonResponse(result)
            else:
                nio_latest = models.NetIOCounterModel.objects.filter(host_id=host_id).order_by('create_time').last()
                delta = now() - nio_latest.create_time
                sent_perm = ( (bytes_sent - nio_latest.bytes_sent) / delta.seconds ) * 60
                recv_perm = ( (bytes_recv - nio_latest.bytes_recv) / delta.seconds ) * 60
                sent_perm = float('{:.3f}'.format(sent_perm))
                recv_perm = float('{:.3f}'.format(recv_perm))
                nio = models.NetIOCounterModel(bytes_sent=bytes_sent,
                                               bytes_recv=bytes_recv,
                                               sent_perm=sent_perm,
                                               recv_perm=recv_perm,
                                               host_id=host_id)

                nio.save()
                result = {
                    'code': 201,
                    'message': '新的网络监控数据插入成功',
                    'data': []
                }
                return JsonResponse(result)


class MemoryDistriView(View):
    """
    实现对内存监控的查询和上报功能
    """

    logger = logger.getChild("MemoryDistriView")

    @method_decorator(ensure_csrf_cookie)
    def get(self,request,host_uuid):
        """
        实现按主键查询和查询最近15天的数据
        """
        # 日志分级与参数解析
        logger = self.logger.getChild('get')
        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)
        logger.info(f"query args host_uuid = {host_uuid} request.GET = {request.GET}")

        if host_id == None:
            # 如果主机信息都不存在，那么监控信息一定是不存在的
            result = {
                'code': 400,
                'message': '当前给定的主机在数据库中没有记录',
                'data': []
            }
            return JsonResponse(result)
        else:
            # 实现针对主键的查询
            if 'pk' in request.GET:
                pk = request.GET.get('pk')
                try:
                    md = models.MemoryDistriModel.objects.get(pk = pk)
                    result = {
                        'code': 200,
                        'message': f'pk = {pk} 的监控数据如下',
                        'data': [{'create_time': md.create_time,
                                  'total': md.total,
                                  'available': md.available,
                                  'used': md.used,
                                  'free': md.free}]
                    }
                    logger.info(f"got recorde {md}")
                    return JsonResponse(result)

                except models.MemoryDistriModel.DoesNotExist:
                    # 如果按 pk 找不到对应的监控数据行，就返回一个空的结果
                    result = {
                        'code': 400,
                        'message': f'pk = {pk} 的监控数据找不到',
                        'data': []
                    }
                    return JsonResponse(result)
            else:
                # 返回最近 15 天的数据
                start_time = now() - timedelta(days=15)
                mds = models.MemoryDistriModel.objects.filetr(create_time__gt=start_time).values(
                                "create_time","total","available","used","free")
                result = {
                    'code': 201,
                    'message': "最近 15 天的监控数据如下",
                    'data': [md for md in mds]
                }
                return JsonResponse(result)

        
        result = {
            'code': 501,
            'message': '触发了未知的异常',
            'data': []
        }
        return JsonResponse(result)
    
    @method_decorator(ensure_csrf_cookie)
    def post(self,request,host_uuid):
        """
        实现上传内存监控数据
        """
        logger = self.logger.getChild('post')
        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)
        logger.info(f"query args host_uuid = {host_uuid} request.POST = {request.POST}")

        if host_id == None:
            logger.info(f"using {host_uuid} can't find any recorde")
            result = {
                'code': 400,
                'message': f"查询不到 {host_uuid} 对应的主机信息",
                'data': []
            }
            return JsonResponse(result)
        else:
            try:
                total = float(request.POST.get('total'))
                available = float(request.POST.get('available'))
                used = float(request.POST.get('used'))
                free = float(request.POST.get('free'))
                md = models.MemoryDistriModel(host_id=host_id,total=total,
                                              available=available,used=used,free=free)
                md.save()

                result = {
                    'code': 200,
                    'message': '数据录入成功',
                    'data': []
                }
                logger.info("memory monitor item saved.")

                return JsonResponse(result)

            except ValueError as err:
                logger.error(f"exception occur during conver data type {err}")
                result = {
                    'code': 500,
                    'message': '数据类型转换时遇到了错误',
                    'data': []
                }
                return JsonResponse(result)
            

class DiskUsageView(View):
    """
    实现对磁盘监控的查询和上报功能
    """
    logger = logger.getChild("DiskUsageView")

    @method_decorator(ensure_csrf_cookie)
    def get(self,request,host_uuid):
        """
        实现对磁盘情况的查询和上报
        """
        logger = self.logger.getChild('get')
        logger.info(f"query args host_uuid = {host_uuid} request.GET = {request.GET}")

        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)

        if host_id == None:
            # 没有主机信息就不会地有监控项信息
            logger.info(f"host info not exists host_uuid = {host_uuid}")
            result = {
                'code': 400,
                'message': '找不到对应的主机信息',
                'data':[]
            }
            return JsonResponse(result)
        else:
            # 有主机信息、看是按 pk 查询还是查询最后 15 天的数据
            if 'pk' in request.GET:
                pk = request.GET.get('pk')
                try:
                    du = models.DiskUsageModel.objects.get(pk = pk)
                    result = {
                        'code': 200,
                        'message': '',
                        'data': [{
                            'mount_point': du.mount_point,
                            'create_time': du.create_time,
                            'total': du.total,
                            'used': du.used,
                            'free': du.free,
                        }]
                    }
                    return JsonResponse(result)
                except models.DiskUsageModel.DoesNotExist:
                    logger.error(f"DiskUsage info not exists pk = {pk}")
                    result = {
                        'code': 400,
                        'message': f'找不到 pk = {pk} 对应的记录',
                        'data': []
                    }
                    return JsonResponse(result)
        
            else:
                start_time = now() - timedelta(days=15)
                dus = models.DiskUsageModel.objects.filter(create_time__gt=start_time).values("create_time",
                                "mount_point",
                                "total",
                                "used",
                                "free")
                result = {
                    'code': 200,
                    'message': '',
                    'data': [du for du in dus]
                }
                return JsonResponse(result)

        result = {
            'code': 501,
            'message': '触发了未知的异常',
            'data': []
        }
        return JsonResponse(result)

    @method_decorator(ensure_csrf_cookie)
    def post(self,request,host_uuid):
        """
        """
        logger = self.logger.getChild('get')
        logger.info(f"query args host_uuid = {host_uuid} request.GET = {request.POST}")

        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)

        if host_id == None:
            logger.info(f"host info not exists host_uuid={host_uuid}")
            result = {
                'code': 400,
                'message': f'host_uuid = {host_uuid} 对应的主机信息查询不到',
                'data': []
            }
            return JsonResponse(result)
        else:
            try:
                mount_point = str(request.POST.get('mount_point'))
                total = int(float(request.POST.get('total')))
                used = int(float(request.POST.get('used')))
                free = int(float(request.POST.get('free')))
                du = models.DiskUsageModel(host_id=host_id,mount_point=mount_point,
                                total=total,used=used,free=free)
                du.save()
                result = {
                    'code': 200,
                    'message': '磁盘使用率监控录入成功',
                    'data': []
                }
                return JsonResponse(result)

            except ValueError as err:
                logger.error(str(err))
                result = {
                    'code': 500,
                    'message': '在进行数据类型转换的时候遇到了异常',
                    'data': []
                }
                return JsonResponse(result)
            except Exception as err:
                logger.error(str(err))
                result = {
                    'code': 501,
                    'message': '触发了未知的异常',
                    'data': []
                }
                return JsonResponse(result)               


class DiskIOCounterView(View):
    """
    实现对磁盘读写计数器的查询和上报
    """
    logger = logger.getChild("DiskIOCounterView")

    @method_decorator(ensure_csrf_cookie)    
    def get(self,request,host_uuid):
        """
        实现对磁盘 IO 计数器的查询
        1、按主键查询
        2、按录入的时间进行查询
        """
        logger = self.logger.getChild('get')
        logger.info(f"query args host_uuid = {host_uuid}  request.GET = {request.GET}")

        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)

        if host_id == None:
            result = {
                'code': 400,
                'message': '找不到 host_uuid 对应的主机信息，没有办法找到对应的磁盘监控',
                'data': []
            }
            return JsonResponse(result)
        else:
            # 有对应的主机信息、要分两种情况 1): 按主键查询  2): 查询最近 15 天的数据
            if 'pk' in request.GET:
                logger.info(f"query recode using pk = {request.GET.get('pk')}")
                try:
                    pk = int(request.GET.get('pk')) # ValueError
                    dic = models.DiskIOCounterModel.objects.get(pk = pk) # DoesNotExist
                except ValueError as err:
                    logger.info("convert pk to int type fail")

                    return JsonResponse({
                        'code': 500,
                        'message': '在把 pk 的值转化为 int 类型时失败',
                        'data': []
                    })
                except models.DiskIOCounterModel.DoesNotExist as err:

                    return JsonResponse({
                        'code': 200,
                        'message': f'找不到 pk = {pk} 对应的记录',
                        'data': []
                    })
                # 成功找到 pk 对应的记录并返回
                return JsonResponse({
                    'code': 200,
                    'message': '',
                    'data': [{
                        'create_time': dic.create_time,
                        'read_count': dic.read_count,
                        'write_count': dic.write_count,
                        'read_bytes': dic.read_bytes,
                        'write_bytes': dic.write_bytes,
                        'read_cps': dic.read_cps,
                        'write_cps': dic.write_cps,
                        'read_kps': dic.read_kps,
                        'write_kps': dic.write_kps,
                    }]
                })
            else:
                # 返回最近 15 天的数据
                start_time = now() - timedelta(days=15)
                dics = modesl.DiskIOCounterModel.objects.filter(create_time__gt=start_time).values(
                    "create_time","read_count","write_count","read_bytes","write_bytes","read_cps","write_cps",
                    "read_kps","write_kps"
                )
                return JsonResponse({
                    'code': 200,
                    'message': '',
                    'data': [dic for dic in dics]
                })
        
        # 保底响应
        return JsonResponse({
            'data': 502,
            'message': '触发了未知的异常',
            'data': []
        })


    @method_decorator(ensure_csrf_cookie)
    def post(self,request,host_uuid):
        """
        实现磁盘 IO 计数器的录入功能
        """
        logger = self.logger.getChild('post')
        logger.info(f"query args host_uuid = {host_uuid} request.POST = {request.POST}")

        host_id = models.HostModel.hosts.get_host_id_by_uuid(host_uuid)

        if host_id == None:
            # 主机信息都不存在，那么就根本没有办法录入磁盘监控信息了
            return JsonResponse({
                'code': 500,
                'message': '主机信息不存在，无法录入磁盘监控信息',
                'data': []
            })

        else:
            # 主机信息存在，可以录入
            dic = models.DiskIOCounterModel.objects.filter(host_id=host_id).order_by('create_time').last()

            # 对参数进行类型转换
            try:
                read_count = int(float(request.POST.get('read_count')))
                write_count = int(float(request.POST.get('write_count')))
                read_bytes = int(float(request.POST.get('read_bytes')))
                write_bytes = int(float(request.POST.get('write_bytes')))
            except ValueError as err:
                logger.error(f"exception occur during convert data type {err}")
                return JsonResponse({
                    'code': 501,
                    'message': '在进行数据类型转换时遇到了问题',
                    'data': []
                })
            
            # 数据类型转换完成之后就可以保存数据了
            if dic == None:
                # 说明当前数据库中还没有磁盘IO的监控数据，那么当前数据将做为第一条数据
                dic = models.DiskIOCounterModel(read_count=read_count,
                        write_count=write_count,
                        read_bytes=read_bytes,
                        write_bytes=write_bytes,
                        read_cps=0,
                        write_cps=0,
                        read_kps=0,
                        write_kps=0,
                        host_id=host_id)
                dic.save()
                return JsonResponse({
                    'code': 200,
                    'message': '当前数据作为第一行数据被录入',
                    'data':[]
                })
            else:
                # 数据库中已经存在监控数据，那么在录入时就要把相关的速率算出来
                # 计算出当前记录与数据库中最新记录的时间差
                seconds = (now() - dic.create_time).seconds

                read_cps = (read_count - dic.read_count)/seconds
                write_cps = (write_count - dic.write_count)/seconds
                read_kps = (read_bytes - dic.read_bytes)/1024/seconds
                write_kps = (write_bytes - dic.write_bytes)/1024/seconds

                dic = models.DiskIOCounterModel(
                    host_id=host_id,
                    read_count=read_count,
                    write_count=write_count,
                    read_bytes=read_bytes,
                    write_bytes=write_bytes,
                    read_cps=read_cps,
                    write_cps=write_cps,
                    read_kps=read_kps,
                    write_kps=write_kps)
                
                dic.save()
                return JsonResponse({
                    'code': 200,
                    'message': '录入成功',
                    'data': []
                })
        
        # 保底响应
        return JsonResponse({
            'code': 505,
            'message': '触发了未知的异常',
            'data': []
        })
    


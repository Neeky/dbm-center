import logging
from django.http import JsonResponse
from django.views import View

from apps.hosts.models.idc import IDC
from apps.hosts.forms.idc import IDCForm

class IDCAddView(View):
    def post(self,request,*args,**kwargs):
        """
        实现添加 IDC 机房信息的功能
        """
        logger = logging.getLogger(__name__)
        idcform = IDCForm(request.POST)
        if idcform.is_valid():
            idcform.save()
            return JsonResponse({'message':'idc 信息增加成功','code':0})
        logger.error("idc 信息增加失败，原因是数据校验没有成功。")
        return JsonResponse({'message':'idc 信息增加失败，原因是数据校验没有成功。','code':0})



        





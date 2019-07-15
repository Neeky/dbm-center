from django.db import models

class IDC(models.Model):
    """
    用于保存 IDC 机房信息
    """
    name = models.CharField(max_length=64,help_text="IDC机房名称",default="深圳宝安机房",null=False)
    city = models.CharField(max_length=64,help_text="IDC机房名称所在的城市名",default="深圳市",null=False)

    class Meta:
        unique_together = ['name','city']
    
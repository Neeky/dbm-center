from django import forms

from . import models

class HostForm(forms.ModelForm):
    """
    与 models.HostModel 对应
    """
    class Meta:
        """
        """
        model = models.HostModel
        fields = "__all__"

class CpuTimesForm(forms.ModelForm):
    """
    """
    class Meta:
        """
        """
        model = models.CpuTimesModel
        fields = "__all__"








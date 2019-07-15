from django.forms import ModelForm
from apps.hosts.models.idc import IDC

__ALL__ = ['IDCForm']

class IDCForm(ModelForm):
    class Meta:
        model = IDC
        fields = '__all__'


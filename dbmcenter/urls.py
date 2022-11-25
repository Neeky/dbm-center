"""dbmcenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.http import HttpResponseRedirect

from dbmcenter.core.tasks.master import init_master

def index(request, *args, **kwargs):
    """
    重定向到 VUE 前端
    """
    return HttpResponseRedirect('dbm-center/index.html')


urlpatterns = [
    path('', index, name='index'),
    path('apis/agents/', include('agents.urls'), name='apis-agents')
]

init_master()
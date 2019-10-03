from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path('',views.HostsView.as_view(),name="hosts-view"),
    path('<uuid:host_uuid>/cpu-times/',views.CpuTimesView.as_view(),name="host-cpu-times-view"),
    path('<uuid:host_uuid>/cpu-frequences/',views.CpuFrequenceView.as_view(),name="host-cpu-frequences-view"),
    path('<uuid:host_uuid>/net-interfaces/',views.NetInterfaceView.as_view(),name="host-net-interfaces-view"),
    path('<uuid:host_uuid>/net-io-counters/',views.NetIOCounterView.as_view(),name="host-net-io-counters-view"),
    path('<uuid:host_uuid>/memory-distributions/',views.MemoryDistriView.as_view(),name="host-memory-distributions-veiw"),
    path('<uuid:host_uuid>/disk-usages/',views.DiskUsageView.as_view(),name="host-disk-usages-view"),
    path('<uuid:host_uuid>/disk-io-counters/',views.DiskIOCounterView.as_view(),name="host-disk-io-counters-view"),
]
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def all_agents(request, *args, **kwargs):
    return JsonResponse({
        'agents': [],
        'message': ''
    })

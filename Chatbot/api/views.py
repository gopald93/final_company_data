from django.http import HttpResponse
from django.shortcuts import render

def api_methods(request):
    context={}
    context["message"]="Api Methods is about the to develop"
    return render(request, "api/api_methods.html",context)    
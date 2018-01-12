from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template


def index(request):
    #t = get_template('base.html')
    return render(request, 'index.html')



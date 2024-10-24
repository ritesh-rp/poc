from django.shortcuts import render
from django.http import HttpResponse
from celeryApp.tasks import add
from datetime import timedelta

from celeryApp.tasks import send_email_fun
from celeryProject import settings

# Create your views here.
def parent(request):
    # add.delay(5,3)
    add.apply_async(args=[5,3],countdown=(5))
    return HttpResponse("celery executed")



def send_email(request):
    send_email_fun.delay("Welcome", "Ritesh Raj", settings.EMAIL_HOST_USER, "riteshp.softprodigy@gmail.com")
    return HttpResponse("Sent Email Successfully...Check your mail please")
from django.urls import path
from celeryApp.views import parent ,send_email

urlpatterns=[
    path("",parent,name='celery'),
    path("mail/",send_email,name='mail')
]
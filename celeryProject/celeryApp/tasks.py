from celery import shared_task
from django.core.mail import send_mail
import time
from django.template.loader import render_to_string



@shared_task(bind=True)
def add(self,a,b):
    for i in range(10): 
        print(i)
    print(f'sum of a and b is {a+b}')
    return a+b



@shared_task(serializer='json', name="send_mail")
def send_email_fun(subject, message, sender, receiver ):
    template= render_to_string('email-template.html',{'name':message})
    # image_path = 'template/images'
    # time.sleep(5) # for check that sending email process runs in background 
    # send_mail(subject, message, sender, [receiver])
    send_mail(subject,message=message,from_email=sender,recipient_list=[receiver], html_message=template)
   
from django.shortcuts import render
from django.http import HttpResponse
from celery_app.tasks import add
from datetime import timedelta
from enrich_service import settings

# Create your views here.
def parent(request):
    # add.delay(5,3)
    add.apply_async(args=[5,3],countdown=(5))
    return HttpResponse("celery executed")
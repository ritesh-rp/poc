import os
from celery import Celery
from datetime import datetime


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celeryProject.settings')
  
app = Celery('celeryProject')
  

app.config_from_object('django.conf:settings',
                       namespace='CELERY')
  
app.autodiscover_tasks()

# @app.task(bind=True)
# def your_task(self,a,b):
#     return a+b
    

# scheduled_datetime = datetime(2023, 6, 14, 12, 0, 0)  # Replace with the desired execution datetime
# your_task.apply_async((4,6),eta=scheduled_datetime)


# CELERY_BEAT_SCHEDULE = {
#     'add-every-2-seconds': {
#         'task': 'celeryProject.your_task',
#         'schedule': datetime(2023, 6, 14, 12, 0, 0),
#         'args': (16, 16),
#     },
# }
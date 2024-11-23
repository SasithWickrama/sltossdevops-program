from __future__ import absolute_import
from celery import Celery


BROKER_URL = 'amqp://celery_usr:celery@localhost:5672/celery'

celery_app = Celery('INITIATE', broker=BROKER_URL, backend='rpc://')


@celery_app.task
def collect_sms_a(args1):
    print('Queue A Started')
    return "success"

@celery_app.task
def collect_sms_b(args1):
    print('Queue B Started')
    return "success"

@celery_app.task
def collect_sms_c(args1):
    print('Queue B Started')
    return "success"
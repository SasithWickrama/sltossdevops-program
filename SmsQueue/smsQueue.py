from __future__ import absolute_import
from celery import Celery
from smsInitiate import SmsInitiate

BROKER_URL = 'amqp://celery_usr:celery@localhost:5672/celery'

celery_app = Celery('INITIATE', broker=BROKER_URL, backend='rpc://')

@celery_app.task
def iptv_sms(data):
    print('IPTV SMS INITIATED')
    result = SmsInitiate.initiateIptvSms(data)
    return result
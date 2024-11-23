from __future__ import absolute_import
from celery import Celery
from projectInitiate import Initiate

BROKER_URL = 'amqp://celery_usr:celery@localhost:5672/celery'

celery_app = Celery('INITIATE', broker=BROKER_URL, backend='rpc://')


@celery_app.task
def initiate_task(projectid):
    print('Project Initiated')
    result = Initiate.initiateTask(projectid)
    return result


@celery_app.task
def start_task():
    print('Task Started')


@celery_app.task
def process_task():
    print('Task Processing')


@celery_app.task
def close_task():
    print('Task Completed')

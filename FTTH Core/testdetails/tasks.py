# we are importing Celery class from celery package
from celery import Celery

# Redis broker URL
BROKER_URL = 'amqp://localhost'

# We are creating an instance of Celery class by passing module name as Restaurant and broker as Redis.
celery_app = Celery('Restaurant', broker=BROKER_URL)

# we are decorating cooking_task function with @celery_app.task decorator.
# Functions which are decorated with @celery_app.task considered celery tasks.
@celery_app.task
def cooking_task(table_no, dishes):
    print("Started cooking for Table Number : "+table_no)
    for dish in dishes:
        print("Cooking : "+dish)
    print("Done cooking for Table Number : "+table_no)

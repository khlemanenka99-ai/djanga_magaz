from celery import shared_task
import logging

logger = logging.getLogger('api')

@shared_task
def add(x, y):
    return x * y

@shared_task
def scheduled_task():
    logger.info('>>> задача выполнена')
    return True


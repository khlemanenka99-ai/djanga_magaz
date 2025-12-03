from celery import shared_task
import logging

import requests

# celery -A myproject worker --loglevel=info команда для запуска воркера
# celery -A myproject beat --loglevel=info команда для запуска расписания для воркера
# celery -A myapp.tasks call dollar_to_byn для вызова одной задачи

logger = logging.getLogger('api')

@shared_task
def add(x, y):
    return x * y

@shared_task
def scheduled_task():
    logger.info('>>> задача выполнена')
    return True

@shared_task(bind=True, max_retries=5, default_retry_delay=10)
def dollar_to_byn(self):
    logger.info("Запуск задачи dollar_to_byn")
    try:
        # API
        url = 'https://api.nbrb.by/exrates/rates/431?periodicity=0'
        response = requests.get(url, timeout=10)
        data = response.json()
        # logger.info(f"Тип data: {type(data)}")
        # logger.info(f"Данные data: {data}")
        rate = (data.get('Cur_OfficialRate'))
        if rate is None:
            raise ValueError("Курс валюты не найден в ответе")
        logger.info(f'Курс: {rate}')
        return rate
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise self.retry(exc=e)




from celery import shared_task
import logging

from celery.worker.state import requests

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

    try:
        # API НБРБ для обменных курсов
        url = 'https://belarusbank.by/api/kursExchange'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # В ответе может быть поле "Cur_OfficialRate"
        rate = data.get('Cur_OfficialRate')
        logger.info(f'>>> задача выполнена, курс равен {rate}')
        return rate
    except Exception as e:
        raise self.retry()
        # Лог или обработка ошибок
    return f"Ошибка при получении курса: {str(e)}"



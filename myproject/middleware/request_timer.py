import logging
import time
from typing import Callable


logger = logging.getLogger('api')

class TimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def timer_deco(func:Callable):
        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            finish = time.time()
            logger.info(f"время обработки запроса = {finish - start}")
            return res
        return wrapper

    @timer_deco
    def __call__(self, request):
        # вызывается при каждом запросе
        logger.info(f"Запрос пришёл: {request.path}")
        # передаём запрос дальше
        response = self.get_response(request)
        # выполняем что-то после обработки view
        logger.info(f"Ответ готов: {response.status_code}")
        # возвращаем ответ пользователю
        return response

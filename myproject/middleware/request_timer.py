import time
from typing import Callable

class TimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def timer_deco(func:Callable):
        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            finish = time.time()
            print(f"время обработки запроса = {finish - start}")
            return res
        return wrapper

    @timer_deco
    def __call__(self, request):
        response = self.get_response(request)
        return response

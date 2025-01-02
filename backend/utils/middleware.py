from typing import Callable
from utils.logger import get_logger
from time import time

logger = get_logger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, app: Callable):
        self.app = app

    def __call__(self, environ: dict, start_response: Callable):
        path = environ.get('PATH_INFO')
        method = environ.get('REQUEST_METHOD')
        start_time = time()

        def logging_start_response(status, headers, exc_info=None):
            duration = int((time() - start_time) * 1000)
            logger.info(
                f'{method} {path} - {status} - {duration}ms'
            )
            return start_response(status, headers, exc_info)

        return self.app(environ, logging_start_response)
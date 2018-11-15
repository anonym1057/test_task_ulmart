
import traceback
import json
import os
import logging

from settings import Settings


class LoggingError():
    """
    Контекстный менеджер для отлавливания ошибок при совершении запроса.
    Ошибки сохраняет  в json
    """
    def __init__(self, url, label,start_time):
        self.url = url
        self.label = label
        self.start_time=start_time


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            error = {
                "timestamp": str(self.start_time),
                "url": self.url,
                "error": {
                    f"exception_type": str(exc_type),
                    "exception_value": str(exc_val),
                    "stack_info": str(traceback.extract_tb(exc_tb))}
            }
            logging.error(str(exc_type) + str(exc_val) + str(traceback.extract_tb(exc_tb)))
            with open(os.path.join(Settings().path_errors, f"log_error_{self.label}.json"), "w") as js:
                json.dump(error, js, ensure_ascii=False)
        return True

import argparse
import os
import requests
from datetime import datetime  as dt
import logging

import pandas as pd

from db import DataBaseMonitoring
from logging_error import LoggingError
from settings import Settings

settings = Settings()
logging.basicConfig(filename=os.path.join(settings.path_log,'log'),level=logging.INFO)

logging.info(f"Starts with settings: {settings.get_settings_dict()}")

def correct_path(file: str):
    """
    Проверяет на правильность пути к файлу
    :param file: путь к файлу
    :return:
    """
    if os.path.isfile(file):
        return file
    else:
        raise argparse.ArgumentTypeError(
            f"file {file} does not exist")


def get_response(url, label, timeout, start_time):
    """
    Делает запрос с адресу.
    Используется контекстный менеджер. Если произошла ошибка, создает файл с подробностями
    :param url: адрес сайта
    :param label: название сайта
    :param timeout: время для запроса
    :param start_time: время начала
    :return:
    """
    with LoggingError(url, label, start_time):
        res = requests.get(url, timeout=timeout)

        return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script ',
        epilog='')

    parser.add_argument(
        'file',
        help='',
        type=correct_path)

    args = parser.parse_args()
    file_xls = args.file

    # скачиваем данные
    data = pd.read_excel(file_xls)
    data = data[data.fetch == True]
    logging.info(f"Data loaded from {file_xls}")

    # открывает бд
    database = DataBaseMonitoring()
    logging.info(f"Data base opened")


    counter={'success':0,'fail':0}
    # по всем адресам
    logging.info("Poll selected addresses")
    for url, label in zip(data.url, data.label):
        start_time = dt.utcnow()
        logging.info(f"Request to {label} ({url}, begins {start_time})")

        res = get_response(url, label, settings.timeout,start_time)
        if res != None:
            logging.info(f"Sucсess: code_status {res.status_code}")

            # если ответ не пустой добавляем его в базу
            database.insert(start_time, url, label, res.elapsed.microseconds, res.status_code,
                            len(res.content) if res.status_code == 200 else None)

            counter['success']+=1
        else:
            logging.error("Fail")
            counter['fail'] += 1

    logging.info(f"poll selected addresses finished: success - {counter['success']} fail - {counter['fail']} ")
    database.print_table(20)
    database.close()

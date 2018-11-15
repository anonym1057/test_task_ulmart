"""
Осуществляет взаимодествие с таблицей Monitoring  с бд  sqlite
"""
import os
import sqlite3
import datetime
import logging

from settings import Settings


class DataBaseMonitoring():
    """
    Осуществляет доступ к базе данных Мониторинг
    """
    def __init__(self):
        self.settings=Settings()
        path_base=os.path.join(self.settings.path_sqlite, f"{self.settings.name_database}.sqlite")
        #проверяем наличие существующей базы данных
        if not os.path.isfile(path_base):
            self.db = self.get_db(path_base)
            #если нет, то создаем скриптом из файла
            with open(os.path.join(
                    os.path.dirname(__file__),'schema.sql')) as f:
                self.db.executescript(f.read())
        else:
            # инициализация базы данных
            self.db = self.get_db(path_base)

    def get_db(self, path):
        """
        Установка соеделения с базой
        :param path:
        :return:
        """
        db = sqlite3.connect(
            path,
            detect_types=sqlite3.PARSE_DECLTYPES)

        db.row_factory = sqlite3.Row
        return db

    def close(self):
        """
        Закрытие соеденения с базой
        :return:
        """
        if not self.db:
            self.db.close()

    def insert(self, ts: type(datetime.datetime.utcnow()), url: str, label: str, response_time: float, status_code: int,
               content_length):
        """
        Добавляет в таблицу информацию и запросе
        :param ts: время, когда бы совершен запрос
        :param url: адрес сайта
        :param label: название сайта
        :param response_time: вермя запроса
        :param status_code: колд ответа
        :param content_length: длина контента
        :return:
        """
        try:
            self.db.execute(
                'insert into MONITORING (TS,URL,LABEL,RESPONSE_TIME,STATUS_CODE,CONTENT_LENGTH) values (?,?,?,?,?,?)',
                (ts, url, label, response_time, status_code, content_length)
            )
            self.db.commit()
        except Exception as e:
            logging.error(str(e))

    def print_table(self, size: int):
        """
        Выводит первые size строк на экран
        :param size: количество строк
        :return:
        """
        if self.settings.print_table:
            lines = self.db.execute("select * from MONITORING").fetchmany(size)
            print(f"Table monitoring first {size} lines")
            if lines:
                print(lines[0].keys())
                for line in lines:
                    for k in line.keys():
                        print(line[k], end='\t')
                    print('')
            else:
                print("Table in empty")


if __name__ == '__main__':
    a = DataBaseMonitoring()
    a.print_table(2)
    a.close()

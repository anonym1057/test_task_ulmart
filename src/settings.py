import os
import configparser
import functools


def singleton(cls):
    instance = None

    @functools.wraps(cls)
    def inner(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return inner


@singleton
class Settings():
    """
    Класс считывает настройки и хранит их
    """

    def __init__(self):
        self.timeout = 10
        self.path_errors = 'errors'
        self.path_log = 'log'
        self.path_sqlite = 'instance'
        self.name_database = 'base'

        config = configparser.ConfigParser()
        try:
            config.read(
                os.path.join(
                    os.path.dirname(__file__),
                    "settings.ini"))
            self.timeout = int(config.get('app', "TIMEOUT"))
            self.path_errors = config.get('app', "PATH_ERRORS")
            self.path_log = config.get('app', "PATH_LOG")
            self.path_sqlite = config.get('app', "PATH_SQLITE")
            self.name_database = config.get('app', "NAME_DATABASE")
        except configparser.Error as e:
            print(str(e))

        if not os.path.exists(self.path_sqlite):
            os.makedirs(self.path_sqlite)

        if not os.path.exists(self.path_errors):
            os.makedirs(self.path_errors)

        if not os.path.exists(self.path_log):
            os.makedirs(self.path_log)

    def get_settings_dict(self):
        return {"TIMEOUT": self.timeout,
                "PATH_ERRORS": self.path_errors,
                "PATH_LOG": self.path_log,
                "PATH_SQLITE": self.path_sqlite,
                "NAME_DATABASE": self.name_database}

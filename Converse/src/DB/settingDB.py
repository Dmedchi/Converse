import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# # путь до папки, где лежит этот модуль
# DB_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
#
# # путь до файла базы данных
# DB_PATH = os.path.join(DB_FOLDER_PATH, 'Server.db')
#
# # создать движок
# engine = create_engine('sqlite:///{}'.format(DB_PATH), echo=False)
#

class DbBaseStorage:
    """Базовый репозиторий"""
    def __init__(self, name, base):
        """
        :param name: Имя базы данных :memory: - создаст базу в памяти
        :param base: базовый класс для создания моделей
        """
        self.name = name
        # Создаем движок
        engine = create_engine('sqlite:///{}'.format(self.name), echo=False)
        # Создаем сессию
        Session = sessionmaker(bind=engine)
        # Создать Session-объект, который привязан к базе данных
        session = Session()
        # Сохраняем текущую сессию
        self.session = session
        # Не забываем создать структуру базы данных
        base.metadata.create_all(engine)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rolback()


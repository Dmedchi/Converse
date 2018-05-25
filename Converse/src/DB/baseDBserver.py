"""БД сервера: декларативное создание таблиц, одноименных классов и их отображения."""

import datetime
from sqlalchemy import  Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Client(Base):
    """Клиент"""

    # Название таблицы
    __tablename__ = 'Client'
    # Первичный ключ
    ClientId = Column(Integer, primary_key=True)
    # Имя клиента
    name = Column(String(25), unique=True)
    # Информация - не обязательное поле
    info = Column(String, nullable=True)

    def __init__(self, name, info=None):
        self.name = name
        if info:
            self.info = info

    def __repr__(self):
        return "<Client('%s')>" % self.name

    def __eq__(self, other):
        # Клиенты равны если равны их имена
        return self.name == other.name


class ClientContacts(Base):
    """Связка контакт-клиент для хранения списка контактов"""

    # Название таблицы
    __tablename__ = 'ClientContacts'
    # Первичный ключ
    ClientContactsId = Column(Integer, primary_key=True)
    # id клиента
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))
    # id контакта клиента
    ContactId = Column(Integer, ForeignKey('Client.ClientId'))

    def __init__(self, client_id, contact_id):
        self.ClientId = client_id
        self.ContactId = contact_id


class ClientHistory(Base):
    """История клиента"""

    # Название таблицы
    __tablename__ = 'ClientHistory'
    # Первичный ключ
    ClientHistoryId = Column(Integer, primary_key=True)
    # IP
    IP = Column(String)
    # Дата входа - по умолчанию текущая
    CreatedDatetime = Column(DateTime, default=datetime.datetime.utcnow)
    # Клиент, чью историю мы храним
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))
    # Для удобного получения клиента по его истории ClientHistory.Client через свойство вместо запроса
    Client = relationship("Client", back_populates="ClientHistories")

    def __init__(self, client_id, ip, creation_datetime=None):
        self.IP = ip
        self.ClientId = client_id
        if creation_datetime:
            self.CreatedDatetime = creation_datetime

    def __repr__(self):
        return "<ClientHistory ('%s', %d)>" % (self.IP, self.ClientId)

    def __eq__(self, other):
        """Истории равны если все совпадает"""
        return self.IP == other.IP and self.CreatedDatetime == other.CreatedDatetime and self.ClientId == other.ClientId

# Обратная связка для получения всех историй клиента Client.ClientHistories через свойство вместо запроса
Client.ClientHistories = relationship("ClientHistory", order_by=ClientHistory.CreatedDatetime,
                                      back_populates="Client")










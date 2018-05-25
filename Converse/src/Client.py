"""
Клиент

Подключается к серверу;
#Формирует presence - сообщение;
# Отправляет presence - сообщение на сервер;
# Получает ответ от сервера;
# Читает или пишет сообщения (в зависимости от того, в каком режиме находится: 'r' или 'w')
"""

import sys
from queue import Queue
import threading
from socket import *
import logging
import log.log_config_Client
from log.class_Log import Log
from Library.lib_ import *
from DB.baseDBclient import Base
from DB.Client_bd import Storage


# Получить логгер клиентa по имени из модуля log_config_Client
client_Logger = logging.getLogger('client')
logg = Log(client_Logger)


class Client:

    def __init__(self, login):
        self.login = login
        self.host = 'localhost'
        self.port = 7777
        self.storage = Storage('{}.db'.format(self.login), Base)
        self.shared_queue = Queue()


    @logg
    def connect(self):
        """Подключиться к серверу."""
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        presence = self.form_presence()
        send_message(self.sock, presence)
        response = get_message(self.sock)
        return response

    def end(self):
        """ Отключиться от сервера."""
        self.sock.close()

    @logg
    def form_presence(self):
        """Сформировать presence - сообщение."""
        presence = Presence(self.login)
        message = presence.form_dict()
        return message

    @logg
    def form_msg(self, to_contact, text):
        """ Создать сообщение."""
        msg = Message(to_contact, self.login, text)
        message = msg.form_dict()
        return message

    @logg
    def get_contacts(self):
        """Получить список контактов."""
        contacts = GetContacts(self.login)
        request = contacts.form_dict()
        send_message(self.sock, request)
        # дальше слушатель получит ответ, который мы получим из очереди
        response = self.shared_queue.get()
        if response['response'] == ACCEPTED:
            contacts = self.shared_queue.get()
            return contacts


    @logg
    def add_contact(self, username):
        """Отправить запрос на добавление контакта на сервер."""
        add_contact = AddContact(self.login, username)
        new_contact = add_contact.form_dict()
        send_message(self.sock, new_contact)
        response = self.shared_queue.get()
        if response['response'] == OK:
            print('Новый контакт {} успешно добавлен'.format(username))
            self.storage.add_contact(username)
            self.storage.commit()

    @logg
    def del_contact(self, username):
        """Отправить запрос на удаление контакта."""
        del_contact = DelContact(self.login, username)
        ex_contact = del_contact.form_dict()
        send_message(self.sock, ex_contact)
        response = self.shared_queue.get()
        if response['response'] == OK:
            print('Контакт {} успешно удален'.format(username))
            self.storage.del_contact(username)
            self.storage.commit()

    @logg
    def send_message(self, to, msg):
        """ Отправить сообщение адресату."""
        message = Message(to, self.login, msg)
        message = message.form_dict()
        send_message(self.sock, message)


if __name__ == '__main__':

    try:
        host = sys.argv[1]
    except IndexError:
        host = 'localhost'
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)
    try:
        login = sys.argv[3]
        print(login)
    except IndexError:
        login = 'Guest'

    user = Client(login)
    user.connect()

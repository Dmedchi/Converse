"""Консольный клиент."""

import sys
import threading
from Client import Client
from base import ConsoleReciever

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
    name = sys.argv[3]
    print(name)
except IndexError:
    name = 'Guest'


user = Client(name)
user.connect()

listener = ConsoleReciever(user.sock, user.shared_queue)
th_listen = threading.Thread(target=listener.poll)
th_listen.daemon = True
th_listen.start()

while True:
    text = input('Введите сообщение: ')
    if text == 'get':
        contacts = user.get_contacts()
        print(contacts)
    elif text.startswith('add'):
        try:
            username = text.split()[1]
        except IndexError:
            print('Вы забыли указать имя контакта.')
        else:
            user.add_contact(username)
    elif text.startswith('del'):
        try:
            username = text.split()[1]
        except IndexError:
            print('Вы забыли указать имя контакта.')
        else:
            user.del_contact(username)
    elif text.startswith('msg'):
        params = text.split()
        try:
            to = params[1]
            msg = params[2]
        except IndexError:
            print('wrong in message')
        else:
            user.send_message(to, msg)
    elif text == 'help':
        print('add <имя пользователя> - добавить контакт')
        print('del <имя пользователя> - удалить контакт')
        print('get - список контактов')
        print('exit - выход')
    elif text == 'exit':
        break
    else:
        print('Неверная команда, для справки введите help')

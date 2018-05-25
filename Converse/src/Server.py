"""
Сервер

Принимает presence - запрос от клиента;
Если presence - запрос соответствует условиям проверки:
    отправляет ​​ответ ​к​лиенту;
    добавляет клиента в список, обслуживает с помощью функции select:
    принимает и обрабатывает поступившие сообщения от клиентов ;
    отправляет ответы в зависимости от поступивших запросов.
"""

import sys
import time
import select
from socket import *
import logging
from log import log_config_Server
from log.class_Log import Log
from Library.lib_ import *
from DB.baseDBserver import Base
from DB.Server_bd import Storage



# Получить логгер серверa по имени из модуля log_config_Server
server_logger = logging.getLogger('server')
logg = Log(server_logger)

class Server:

    @logg
    def __init__(self, host, port):
        """Настроить сервер."""
        self.host = host
        self.port = port
        self.sock = self._run()
        self.clients = []
        self.storage = Storage('Server.db', Base)
        self.names = {}


    def _run(self):
        """Запустить работу сокета на сервере."""
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(15)
        sock.settimeout(0.2)
        return sock

    @logg
    def read_requests(self, r_clients):
        """Читать сообщения."""
        messages = []
        for sock in r_clients:
            try:
                message = get_message(sock)
                messages.append((message, sock))
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                self.clients.remove(sock)
        return messages

    @logg
    def write_responses(self, messages):
        """Отправлять сообщения тем клиентам, от которых поступили запросы."""
        for message, sock in messages:

            if message['action'] == GET_CONTACTS:
                username = message['account_name']
                contacts = self.storage.get_contacts(username)
                respect = Response(ACCEPTED, num=len(contacts))
                response = respect.form_response()
                send_message(sock, response)
                # for contact in contacts:
                #     print(contact)
                send_message(sock, contacts)

            elif message['action'] == ADD_CONTACT:
                client_username = message['account_name']
                contact_username = message['user_id']
                self.storage.add_contact(client_username, contact_username)
                self.storage.commit()
                good = Response(OK)
                response = good.form_response()
                send_message(sock, response)


            elif message['action'] == DEL_CONTACT:
                client_username = message['account_name']
                contact_username = message['user_id']
                self.storage.del_contact(client_username, contact_username)
                self.storage.commit()
                good = Response(OK)
                response = good.form_response()
                send_message(sock, response)

            elif message['action'] == MSG:
                # получить контакт, которому надо отправить сообщение
                to = message[TO]
                # получить по имени сокет
                client_sock = self.names[to]
                send_message(client_sock, message)
                # ответить тому, кто прислал сообщение, что все хорошо
                response = Response(ACCEPTED)
                send_message(sock, response.form_response())


    def connection(self):
        """Настроить подключение."""
        try:
            conn, addr = self.sock.accept()
            print("Получен запрос на соединение от %s" % str(addr))
            msg = get_message(conn)
            if msg['action'] == PRESENCE:
                # Получаем имя пользователя
                client_name = msg['account_name']
                print('К нам подключился {}'.format(client_name))
                # если клиента нету в базе
                # print(self.storage.client_exists(client_name))
                if not self.storage.client_exists(client_name):
                    print('Добавляем нового клиента')
                    self.storage.add_client(client_name)
                    print('Сохраняем')
                    self.storage.commit()
                # добавляем историю подключения
                self.storage.add_history(client_name, addr[0])
                self.storage.commit()
                # отправляем ответ
                r = Response('ok')
                response = r.form_response()
                send_message(conn, response)
            else:
                r = Response('wrong_request')
                response = r.form_response()
                send_message(conn, response)
                self.clients.append(conn)
        except OSError as err:
            pass
        else:
            # Добавляем клиента в список
            self.clients.append(conn)
            # Добавляем в словарь имя клиента и соответствующий ему сокет
            self.names[client_name] = conn

        finally:
            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(self.clients, self.clients, [], wait)
            except Exception as e:
                pass

            requests = self.read_requests(r)
            self.write_responses(requests)

    def main_loop(self):
        """Главный цикл работы сервера"""
        print('Сервер запущен!')
        while True:
            self.connection()


if __name__ == '__main__':

    try:
        host = sys.argv[1]
    except IndexError:
        host = ''
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        sys.exit(0)

    server = Server(host, port)
    server.main_loop()



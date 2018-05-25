"""Консольный и GUI обработчик входящих сообщений."""

from Library.lib_ import *
from PyQt5.QtCore import QObject, pyqtSignal


class Receiver:
    """Класс-получатель информации из сокета"""

    def __init__(self, sock, shared_queue):
        # запоминаем очередь ответов
        self.shared_queue = shared_queue
        # запоминаем сокет
        self.sock = sock
        self.is_alive = False

    def process_message(self, message):
        """Будет переопределена в других классах"""
        pass

    def poll(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            data = self.sock.recv(1024)
            # print('----------------->', data)
            if data:
                try:
                    # Если нам пришло сообщение
                    msg = bytes_str_dict(data)
                    # Если это message
                    if 'action' in msg and msg['action'] == MSG:
                        # Печатаем в нормальном виде
                        self.process_message(msg)
                    else:
                        # Добавляем сообщение в очередь т.к. это серверное сообщение
                        self.shared_queue.put(msg)
                except Exception:
                    # Если нам пришел ответ от сервера мы его добавляем в очередь для дальнейшей обработки
                    resp = bytes_str_dict(data)
                    # При этом поток приостанавливается
                    self.shared_queue.put(resp)
            else:
                break

    def stop(self):
        self.is_alive = False


class ConsoleReciever(Receiver):
    """Консольный обработчик входящих сообщений."""

    def process_message(self, message):
        """Отобразить текст сообщения в консоль и от кого оно пришло."""
        print(">> от {}: {}".format(message[FROM], message[MESSAGE]))



class GuiRecieverSimple(Receiver):

    def __init__(self, sock, shared_queue, list_vidget):
        self.list_vidget = list_vidget
        Receiver.__init__(self, sock, shared_queue)
        QObject.__init__(self)

    def process_message(self, message):
        self.list_vidget.addItem(str(message))

    def poll(self):
        super().poll()
        self.finished.emit(0)



class GuiReciever(Receiver, QObject):
    """GUI обработчик входящих сообщений."""

    data = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, sock, shared_queue):
        Receiver.__init__(self, sock, shared_queue)
        QObject.__init__(self)

    def process_message(self, message):
        self.data.emit('{} >>> {}'.format(message[FROM], message[MESSAGE]))


    def poll(self):
        super().poll()
        self.finished.emit(0)





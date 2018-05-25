"""Клиент с графическим интерфейсом."""

import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore, uic
# import threading
from PyQt5.QtCore import Qt, QThread, pyqtSlot, pyqtSignal
from base import GuiReciever
from Client import Client
from setting_window import window

def get_name():
    """Получить имя и создать клиента"""
    login, ok = QtWidgets.QInputDialog.getText(window,
                                             'Start',
                                             'login: ',
                                              text='')
    if ok:
        window.setWindowTitle(login)
        user = Client(login=login)
        return user

# создать приложение
app = QtWidgets.QApplication(sys.argv)

# создать заставку
splash = QtWidgets.QSplashScreen(QtGui.QPixmap("icons/star513.png"))

# Имитация процесса
def load_data(splash):
    """Загрузка данных."""
    for i in range(1, 3):
        time.sleep(1)
        splash.showMessage("подключение...{}".format(i),
                               QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
        QtWidgets.qApp.processEvents()

# Отобразить заставку
splash.show()

# Запустить оборот цикла
QtWidgets.qApp.processEvents()

# Загрузить 'данные'
load_data(splash)

# Закрыть заставку и загрузить основное окно
splash.finish(window)

# Создать клиента и подключиться к серверу
user = get_name()
user.connect()

listener = GuiReciever(user.sock, user.shared_queue)

# Связать сигнал и слот:
# 1. Слот: обновление данных в списке сообщений
@pyqtSlot(str)
def show_chat(data):
    """Отобразить сообщения в истории."""
    try:
        msg = data
        window.storyMessage.addItem(msg)
    except Exception as e:
        print('Error in show_chat: ', e)

# 2. Сигнал из GuiReciever
listener.data.connect(show_chat)
th = QThread()
listener.moveToThread(th)
th.started.connect(listener.poll)
th.start()


# получить список контактов
contacts = user.get_contacts()

def list_contacts(contacts):
    """Отобразить список контактов."""
    window.listWidget.clear()
    try:
        for contact in contacts:
            window.listWidget.addItem(contact)
    except TypeError:
        pass

list_contacts(contacts)


def add_contact():
    """Добавить контакт."""
    try:
        username = window.textEdit.toPlainText()
        if username:
            user.add_contact(username)
            window.listWidget.addItem(username)
    except Exception as e:
        print('error in add: ', e)

window.ButtonAdd.clicked.connect(add_contact)
window.ButtonAdd.clicked.connect(window.textEdit.clear)


def delete_contact():
    """Удалить контакт."""
    try:
        current_item = window.listWidget.currentItem()
        username = current_item.text()
        user.del_contact(username)
        current_item = window.listWidget.takeItem(window.listWidget.row(current_item))
        del current_item
    except Exception as e:
        print('error in del:', e)

window.ButtonDelete.clicked.connect(delete_contact)


def send():
    """Отправить сообщение."""
    text = window.InputText.toPlainText()
    if text:
        # получить выделенного пользователя
        selected_index = window.listWidget.currentIndex()
        # получить имя пользователя
        name = selected_index.data()
        # отправить сообщение
        user.send_message(name, text)
        msg = '{} >>> {}'.format(user, text)

window.ButtonSend.clicked.connect(send)
window.ButtonSend.clicked.connect(window.InputText.clear)


window.show()

sys.exit(app.exec_())











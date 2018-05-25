import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QLabel, QFileDialog
from PyQt5.QtGui import QIcon, QFont, QPixmap


app = QApplication(sys.argv)
window = uic.loadUi('Window.ui')


openFile = QAction('Avatar', window)
openFile.setStatusTip('Открыть файл')
openFile.triggered.connect(lambda: showDialog())

menubar = window.menuBar()
fileMenu = menubar.addMenu('File')
fileMenu.addAction(openFile)

def showDialog():
    fname = QFileDialog.getOpenFileName(window, 'File')[0]
    pixmap = QPixmap(fname)
    window.avatar.setPixmap(pixmap)

# icons
smile = QAction(QIcon('smile.png'), 'Smile', window)
window.smileBt.addAction(smile)
window.smileBt.clicked.connect(lambda: addSmile('icons/smile.png'))

tongue = QAction(QIcon("tongue.png"), 'Tongue', window)
window.tongueBt.addAction(smile)
window.tongueBt.clicked.connect(lambda: addSmile("icons/tongue.png"))

wink = QAction(QIcon('wink.png'), 'Wink', window)
window.winkBt.addAction(wink)
window.winkBt.clicked.connect(lambda: addSmile('icons/wink.png'))

indifferent = QAction(QIcon('indifferent.png'), 'Indifferent', window)
window.smileBt.addAction(indifferent)
window.indifferentBt.clicked.connect(lambda: addSmile('icons/indifferent.png'))

kiss = QAction(QIcon("kiss.png"), 'Kiss', window)
window.kissBt.addAction(kiss)
window.kissBt.clicked.connect(lambda: addSmile("icons/kiss.png"))

suspect = QAction(QIcon('suspect.png'), 'Suspect', window)
window.suspectBt.addAction(suspect)
window.suspectBt.clicked.connect(lambda: addSmile('icons/suspect.png'))

dead = QAction(QIcon('dead.png'), 'Dead', window)
window.deadBt.addAction(dead)
window.deadBt.clicked.connect(lambda: addSmile('icons/dead.png'))

flower = QAction(QIcon('flower.png'), 'Flower', window)
window.flowerBt.addAction(flower)
window.flowerBt.clicked.connect(lambda: addSmile('icons/flower.png'))

flowers = QAction(QIcon('flowers.png'), 'Flowers', window)
window.flowersBt.addAction(flowers)
window.flowersBt.clicked.connect(lambda: addSmile('icons/flowers.png'))

chocolate = QAction(QIcon('chocolate.png'), 'Chocolate', window)
window.chocolateBt.addAction(chocolate)
window.chocolateBt.clicked.connect(lambda: addSmile('icons/chocolate.png'))


def addSmile(url):
    window.InputText.textCursor().insertHtml('<img src="%s" /> ' % url)



# format text
bold = QAction(QIcon('b.jpg'), 'Bold', window)
window.boldBt.addAction(bold)
window.boldBt.clicked.connect(lambda: addFormat('b'))

italic = QAction(QIcon('i.jpg'), 'Italic', window)
window.italicBt.addAction(italic)
window.italicBt.clicked.connect(lambda: addFormat('i'))

underlined = QAction(QIcon('u.jpg'), 'Underlined', window)
window.underlinedBt.addAction(underlined)
window.underlinedBt.clicked.connect(lambda: addFormat('u'))

def addFormat(tag):
    selected_text = window.InputText.textCursor().selectedText()
    window.InputText.textCursor().insertHtml('<{tag}>{val}</{tag}>'.format(val=selected_text, tag=tag))


if __name__ == '__main__':
    window.show()
    sys.exit(app.exec_())
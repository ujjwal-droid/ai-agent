from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel, QLineEdit, QSizePolicy, QFrame, QHBoxLayout, QStackedWidget,QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont,QPainter, QMovie, QTextCharFormat, QTextBlockFormat, QColor
from PyQt5.QtCore import Qt, QTimer, QSize
from dotenv import dotenv_values
import sys
import os


env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message =""
TempDirPath = rf"{current_dir}\frontend\graphics"
GraphicsDirPath = rf"{current_dir}\frontend\graphics"



    
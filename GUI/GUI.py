# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import threading, sys, os, time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scripts import tofig, extract, train, convert, merge
from tools import utils
from queue import Queue

'''
            ██╗  ██╗██╗   ██╗ █████╗ ███████╗██████╗  ██████╗
            ██║ ██╔╝██║   ██║██╔══██╗██╔════╝██╔══██╗██╔════╝ 
            █████╔╝ ██║   ██║███████║█████╗  ██████╔╝██║  ███╗
            ██╔═██╗ ██║   ██║██╔══██║██╔══╝  ██╔══██╗██║   ██║
            ██║  ██╗╚██████╔╝██║  ██║███████╗██║  ██║╚██████╔╝
            ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝
            
MainWindow ：主窗口
    centralwidget ：中心界面部件
    
        pushButton_4 ：关闭按钮
        pushButton_5 ：最小化按钮
        
    widget_2 ：操作面板外层布局
    
        widget ：内层布局（“选择素材文件，选择目标文件，选择输出文件夹”）
        
            horizontalLayout ：水平布局1
            
                horizontalSpacer_2 ：间隔控制组件
                horizontalSpacer_8 ：间隔控制组件
                label ：标签（“选择素材文件”）
                lineEdit ：输入框1
                pushButton ：按钮1-弹出文件选择
                
            horizontalLayout_2 ：水平布局2
            
                horizontalSpacer_3 ：间隔控制组件
                horizontalSpacer_5 ：间隔控制组件
                label_2 ：标签（“选择目标文件”）
                lineEdit_2 ：输入框2
                pushButton_7 ：按钮2-弹出文件选择
                
            horizontalLayout_3 ：水平布局3
            
                horizontalSpacer_10 ：间隔控制组件
                horizontalSpacer_6 ：间隔控制组件
                horizontalSpacer_7 ：间隔控制组件
                horizontalSpacer_9 ：间隔控制组件
                label_4 ：标签（“选择输出文件夹”）
                lineEdit_3 ：输入框3
                pushButton_6 ：按钮3-弹出路径选择
                
        widget_3 ：内层布局（“开始预处理，开始训练，开始合成”）
        
            horizontalSpacer_11 ：间隔控制组件
            horizontalSpacer_12 ：间隔控制组件
            pushButton_10 ：按钮4-开始合成
            pushButton_8 ：按钮5-开始训练
            pushButton_9 ：按钮6-开始预处理
        

'''

state = Queue()
thr_train, thr_convert, thr_preprocess = None, None, None

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))

class Ui_MainWindow(QMainWindow,QtWidgets.QWidget):   #主窗口
    path = {'target' : None, 'source' : None, 'savepath' : None}

    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi(self)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)

    def normalOutputWritten(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    @pyqtSlot(str)
    def upDateMessage(self, message):
        self.textEdit.append(message)

    def setupUi(self, MainWindow):
        self.extension_list = ('avi','flv','mkv','mov','mp4','mpeg','webm')
        MainWindow.setObjectName("Face-Stealer")
        MainWindow.setEnabled(True)
        MainWindow.resize(440, 800)
        MainWindow.setMinimumSize(QtCore.QSize(440, 800))
        MainWindow.setMaximumSize(QtCore.QSize(440, 800))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setStyleSheet("")
        #中心界面主体设置开始
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("QWidget{\n"
"\n"
"        background-image: url(E:/Nutstore/Python/Pycharm_Project/Kaqiusha_Project/GUI/back.jpg);\n"   #中心界面的QSS美化
"\n"
"        \n"
"        border-top-right-radius:10px;\n"
"        border-bottom-right-radius:10px;\n"
"        border-top-left-radius:10px;\n"
"        border-bottom-left-radius:10px;\n"
"    }\n"
    
"\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        
        '''console'''
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setFontWeight(100)
        self.textEdit.setStyleSheet('QTextEdit{font-size:13px; background: #333; color:white; font-family:Courier New, Microsoft YaHei;}')
        self.textEdit.setGeometry(QtCore.QRect(0, 320, 440, 450))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        self.textEdit.setPlainText(
'--------------------欢迎使用本软件-------------------\n'
' ██╗  ██╗██╗   ██╗ █████╗ ███████╗██████╗  ██████╗ \n'
' ██║ ██╔╝██║   ██║██╔══██╗██╔════╝██╔══██╗██╔════╝ \n'
' █████╔╝ ██║   ██║███████║█████╗  ██████╔╝██║  ███╗\n'
' ██╔═██╗ ██║   ██║██╔══██║██╔══╝  ██╔══██╗██║   ██║\n'
' ██║  ██╗╚██████╔╝██║  ██║███████╗██║  ██║╚██████╔╝\n'
' ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ \n'
'--------------------FACE STEALER-------------------\n'
                                                   '\n'
        )
#         self.textEdit.setPlainText(
# '    (\_/)-----------------------------------------------(\_/)\n'
# '   (=\'.\'=)                      欢迎使用本软件                     (=\'.\'=) \n'
# '   (")_(")----------------------------------------------(")_(")\n'
#           )
        '''console'''

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)   #pushButton_4 ：右上角关闭按钮
        self.pushButton_4.setGeometry(QtCore.QRect(410, 10, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton{background:rgb(11,192,255);border-radius:5px;\n"
                                        "\n"
                                        "\n"
                                        "}QPushButton:hover{background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.815, fx:0.5, fy:0.5, stop:0.221591 rgba(185, 185, 185, 255), stop:0.948864 rgba(225, 225, 225, 255));}\n"
                                        "")   #按钮QSS美化
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)   #pushButton_5 ：右上角最小化按钮
        self.pushButton_5.setGeometry(QtCore.QRect(380, 10, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("QPushButton{background:rgb(239, 239, 239);border-radius:5px;\n"
                                        "\n"
                                        "\n"
                                        "}QPushButton:hover{background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.815, fx:0.5, fy:0.5, stop:0.221591 rgba(185, 185, 185, 255), stop:0.948864 rgba(225, 225, 225, 255));}\n"
                                        "")   #按钮QSS美化
        self.pushButton_5.setObjectName("pushButton_5")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(-40, 120, 541, 201))
        self.widget_2.setAutoFillBackground(False)
        self.widget_2.setStyleSheet("QWidget{\n"
"        color:#000000;\n"
"        background-image: url(E:/Nutstore/Python/Pycharm_Project/Kaqiusha_Project/GUI/008.png);\n"
"        \n"
"        border-top:1px solid darkGray;\n"
"        border-bottom:1px solid darkGray;\n"
"        border-right:1px solid darkGray;\n"

"        border-left:1px solid darkGray;\n"

"        \n"
"    }\n"
"\n"
"\n"
"")
        self.widget_2.setObjectName("widget_2")
        self.widget = QtWidgets.QWidget(self.widget_2)
        self.widget.setGeometry(QtCore.QRect(50, -10, 421, 151))
        self.widget.setStyleSheet("QWidget{\n"
"    border:0;\n"
"\n"
"}\n"
"")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setFamily("方正粗宋简体")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{border:0;\n"
"    color: rgb(63, 63, 63);\n"
"}")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setStyleSheet("QLineEdit{background:#4c4b4b; color:white;\n"
"        border-top:1px solid darkGray;\n"
"        border-bottom:1px solid darkGray;\n"
"        border-right:1px solid darkGray;\n"
"        border-top-right-radius:4px;\n"
"        border-bottom-right-radius:4px;\n"
"        border-left:1px solid darkGray;\n"
"        border-top-left-radius:4px;\n"
"        border-bottom-left-radius:4px;\n"
"\n"
"}")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setEnabled(True)
        self.pushButton.setMinimumSize(QtCore.QSize(50, 20))
        self.pushButton.setMaximumSize(QtCore.QSize(50, 20))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("QPushButton\n"
                                      "{\n"
                                      "    background:rgb(255,255,255);\n"
                                      "\n"
                                      "        border-top-right-radius:5px;\n"
                                      "        border-bottom-right-radius:5px;\n"
                                      "        border-top-left-radius:5px;\n"
                                      "        border-bottom-left-radius:5px;\n"
                                      "\n"
                                      "}\n"
                                      "QPushButton:hover{background:rgb(208,208,208);}\n"
                                      "")
        self.pushButton.setIconSize(QtCore.QSize(16, 16))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.get_source_filename)
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 0, 10, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setFamily("方正粗宋简体")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel{border:0;\n"
"    color: rgb(63, 63, 63);\n"
"}")
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem2 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        
        self.lineEdit_2.setStyleSheet("QLineEdit{background:#4c4b4b; color:white;\n"
"        border-top:1px solid darkGray;\n"
"        border-bottom:1px solid darkGray;\n"
"        border-right:1px solid darkGray;\n"
"        border-top-right-radius:4px;\n"
"        border-bottom-right-radius:4px;\n"
"        border-left:1px solid darkGray;\n"
"        border-top-left-radius:4px;\n"
"        border-bottom-left-radius:4px;\n"
"\n"
"}")
        self.lineEdit_2.setObjectName("lineEdit_2")
        
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButton_7 = QtWidgets.QPushButton(self.widget)
        self.pushButton_7.setEnabled(True)
        self.pushButton_7.setMinimumSize(QtCore.QSize(50, 20))
        self.pushButton_7.setMaximumSize(QtCore.QSize(50, 20))
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_7.setStyleSheet("QPushButton\n"
                                        "{\n"
                                        "    background:rgb(255,255,255);\n"
                                        "\n"
                                        "        border-top-right-radius:5px;\n"
                                        "        border-bottom-right-radius:5px;\n"
                                        "        border-top-left-radius:5px;\n"
                                        "        border-bottom-left-radius:5px;\n"
                                        "\n"
                                        "}\n"
                                        "QPushButton:hover{background:rgb(208,208,208);}\n"
                                        "")
        self.pushButton_7.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.get_target_filename)
        self.horizontalLayout_2.addWidget(self.pushButton_7)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(3, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setMaximumSize(QtCore.QSize(120, 20))
        font = QtGui.QFont()
        font.setFamily("方正粗宋简体")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("QLabel{border:0;\n"
"\n"
"    color: rgb(63, 63, 63);\n"
"}")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        spacerItem5 = QtWidgets.QSpacerItem(7, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setStyleSheet("QLineEdit{background:#4c4b4b; color:white;\n"
"        border-top:1px solid darkGray;\n"
"        border-bottom:1px solid darkGray;\n"
"        border-right:1px solid darkGray;\n"
"        border-top-right-radius:4px;\n"
"        border-bottom-right-radius:4px;\n"
"        border-left:1px solid darkGray;\n"
"        border-top-left-radius:4px;\n"
"        border-bottom-left-radius:4px;\n"
"\n"
"}")
        self.lineEdit_3.setObjectName("lineEdit_3")

        
        self.horizontalLayout_3.addWidget(self.lineEdit_3)
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.pushButton_6 = QtWidgets.QPushButton(self.widget)
        self.pushButton_6.setEnabled(True)
        self.pushButton_6.setMinimumSize(QtCore.QSize(50, 20))
        self.pushButton_6.setMaximumSize(QtCore.QSize(50, 20))
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_6.setStyleSheet("QPushButton\n"
                                        "{\n"
                                        "    background:rgb(255,255,255);\n"
                                        "\n"
                                        "        border-top-right-radius:5px;\n"
                                        "        border-bottom-right-radius:5px;\n"
                                        "        border-top-left-radius:5px;\n"
                                        "        border-bottom-left-radius:5px;\n"
                                        "\n"
                                        "}\n"
                                        "QPushButton:hover{background:rgb(208,208,208);}\n"
                                        "")
        self.pushButton_6.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.get_path)
        self.horizontalLayout_3.addWidget(self.pushButton_6)
        spacerItem7 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setGeometry(QtCore.QRect(55, 130, 411, 60))   #     ！！！    容器Widget_3的位置和大小，此处需调整。
        self.widget_3.setStyleSheet("QWidget{\n"
"    border:0;\n"
"\n"
"}\n"
"")
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_9 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_9.setEnabled(True)
        self.pushButton_9.setMinimumSize(QtCore.QSize(110, 50))
        self.pushButton_9.setMaximumSize(QtCore.QSize(500, 500))
        font = QtGui.QFont()
        font.setFamily("方正粗宋简体")
        font.setPointSize(14)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_9.setAutoFillBackground(False)
        self.pushButton_9.setStyleSheet(" QPushButton\n"
                                        "{\n"
                                        "    background:#ffffff;\n"
                                        "    margin-top:4px;\n"
                                        "    margin-bottom:4px;\n"
                                        "    color: rgb(63, 63, 63);\n"

                                        "\n"
                                        "}\n"
                                        "QPushButton:hover{background:rgb(220,220,220);}\n"
                                        "")
        self.pushButton_9.setIconSize(QtCore.QSize(100, 100))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.clicked.connect(self.preprocess_start)
        self.horizontalLayout_4.addWidget(self.pushButton_9)
        spacerItem8 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.pushButton_8 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_8.setEnabled(True)
        self.pushButton_8.setMinimumSize(QtCore.QSize(110, 50))
        self.pushButton_8.setMaximumSize(QtCore.QSize(500, 500))
        font = QtGui.QFont()
        font.setFamily("方正粗宋简体")
        font.setPointSize(14)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_8.setAutoFillBackground(False)
        self.pushButton_8.setStyleSheet(" QPushButton\n"
                                        "{\n"
                                        "    background:#ffffff;\n"
                                        "    margin-top:4px;\n"
                                        "    margin-bottom:4px;\n"
                                        "    color: rgb(63, 63, 63);\n"
 
                                        "\n"
                                        "}\n"
                                        "QPushButton:hover{background:rgb(220,220,220);}\n"
                                        "")
        self.pushButton_8.setIconSize(QtCore.QSize(100, 100))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(self.training_start)
        self.horizontalLayout_4.addWidget(self.pushButton_8)
        spacerItem9 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.pushButton_10 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_10.setEnabled(True)
        self.pushButton_10.setMinimumSize(QtCore.QSize(110, 50))
        self.pushButton_10.setMaximumSize(QtCore.QSize(500, 500))
        font = QtGui.QFont()
        font.setFamily("方正粗宋简体")
        font.setPointSize(14)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_10.setAutoFillBackground(False)
        self.pushButton_10.setStyleSheet(" QPushButton\n"
                                        "{\n"
                                        "    background:#ffffff;\n"
                                        "    margin-top:4px;\n"
                                        "    margin-bottom:4px;\n"
                                        "    color: rgb(63, 63, 63);\n"
   
                                        "\n"
                                        "}\n"
                                        "QPushButton:hover{background:rgb(220,220,220);}\n"
                                        "")
        self.pushButton_10.setIconSize(QtCore.QSize(100, 100))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.clicked.connect(self.merging_start)
        self.horizontalLayout_4.addWidget(self.pushButton_10)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 440, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.pushButton_4.clicked.connect(MainWindow.close)
        self.pushButton_5.clicked.connect(MainWindow.showMinimized)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)             # 隐藏边框

    def get_path(self):   #获取文件路径

        directory = QFileDialog.getExistingDirectory(self, "注意!选择文件路径！!", "/")
        self.lineEdit_3.setText(directory)
        self.path['savepath'] = directory
        
    def get_source_filename(self):   #获取素材文件名和后缀名
        filename, filetype = QFileDialog.getOpenFileName(self, "选择素材文件", "/")
        if filename.endswith(self.extension_list):
            self.lineEdit.setText(filename)
            self.path['source'] = filename
        elif not filename.endswith(self.extension_list) and filetype:
            self.message('注意！', '请选择以下格式的视频文件：\navi, flv, mkv, mov, mp4, mpeg, webm', '确定')

    def get_target_filename(self):    #获取目标文件名和后缀名
        filename, filetype = QFileDialog.getOpenFileName(self, "选择目标文件", "/")
        if filename.endswith(self.extension_list):
            self.lineEdit_2.setText(filename)
            self.path['target'] = filename
        elif not filename.endswith(self.extension_list) and filetype:
            self.message('注意！', '请选择以下格式的视频文件：\navi, flv, mkv, mov, mp4, mpeg, webm', '确定')

    def preprocess_start(self):   #开始预处理  并改成停止预处理按钮
        if self.path_check() and self.threading_manager('preprocessing'):
            _translate = QtCore.QCoreApplication.translate
            self.pushButton_9.setText(_translate("MainWindow", "停止预处理"))
            self.pushButton_9.clicked.disconnect()
            self.pushButton_9.clicked.connect(self.preprocess_stop)
        elif not self.path_check():
            self.message('注意！', '请输入三个完整路径', '确定')

    def training_start(self):    #开始训练  并改成停止训练按钮
        if self.path_check() and self.threading_manager('train'):
            _translate = QtCore.QCoreApplication.translate
            self.pushButton_8.setText(_translate("MainWindow", "停止训练"))
            self.pushButton_8.clicked.disconnect()
            self.pushButton_8.clicked.connect(self.training_stop)
        elif not self.path_check():
            self.message('注意！', '请输入三个完整路径', '确定')

    def merging_start(self):  # 开始合成  并改成停止合成按钮
        if self.path_check() and self.threading_manager('convert'):
            _translate = QtCore.QCoreApplication.translate
            self.pushButton_10.setText(_translate("MainWindow", "停止合成"))
            self.pushButton_10.clicked.disconnect()
            self.pushButton_10.clicked.connect(self.merging_stop)
        elif not self.path_check():
            self.message('注意！', '请输入三个完整路径', '确定')

    def preprocess_stop(self):    #停止预处理  并改成开始预处理按钮
        print('停止预处理中……………………')
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_9.setText(_translate("MainWindow", "开始预处理"))
        self.pushButton_9.clicked.disconnect()
        self.pushButton_9.clicked.connect(self.preprocess_start)
        state.put('stop_pre')
        state.put('stop_pre')

    def training_stop(self):     #停止训练  并改成开始训练按钮
        print('停止训练中……………………')
        state.put('stop_tra')
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_8.setText(_translate("MainWindow", "开始训练"))
        self.pushButton_8.clicked.disconnect()
        self.pushButton_8.clicked.connect(self.training_start)

    def merging_stop(self):     #停止合成  并改成开始合成按钮
        print('停止合成中……………………')
        state.put('stop_con')
        state.put('stop_con')
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_10.setText(_translate("MainWindow", "开始合成"))
        self.pushButton_10.clicked.disconnect()
        self.pushButton_10.clicked.connect(self.merging_start)

    def path_list(self):
        path_list = []
        for value in self.path.values():
            path_list.append(value)
        path_list.insert(2, 'model')
        return path_list

    def path_check(self):
        path_flag = 0
        for value in self.path.values():
            if value:
                path_flag += 1
        return path_flag == 3

    def dir_check(self, dir):
        Ready_flag = True
        if dir == 'm':
            if not os.path.exists(utils.get_dir(self.path_list(), 'e_t')) or not os.path.exists(utils.get_dir(self.path_list(), 'e_r')):
                Ready_flag = False
                print('未能成功读取面部识别文件，请进行预处理')
        elif dir == 'c':
            if not os.path.exists(utils.get_dir(self.path_list(), 't')) or not os.path.exists(utils.get_dir(self.path_list(), 'r')):
                Ready_flag = False
                print('未能成功读取预处理文件，请进行预处理')
            if not os.path.exists(utils.get_dir(self.path_list(), 'm')):
                Ready_flag = False
                print('未能成功读取训练模型文件，请进行训练')
        return Ready_flag

    def message(self, title, text, button):
        self.messageBox = QMessageBox()
        self.messageBox.setWindowTitle(title)
        self.messageBox.setText(text)
        self.messageBox.addButton(QtWidgets.QPushButton(button), QMessageBox.YesRole)
        self.messageBox.setStyleSheet("QLabel{margin-right:22px;}")
        self.messageBox.exec_()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  #更改鼠标图标
            
    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.centralwidget.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Face-Stealer</span></p></body></html>"))
        self.pushButton_4.setText(_translate("MainWindow", "×"))
        self.pushButton_5.setText(_translate("MainWindow", "-"))
        self.label.setText(_translate("MainWindow", "选择目标文件"))
        self.pushButton.setText(_translate("MainWindow", "..."))
        self.label_2.setText(_translate("MainWindow", "选择素材文件"))
        self.pushButton_7.setText(_translate("MainWindow", "..."))
        self.label_4.setText(_translate("MainWindow", "选择输出文件夹"))
        self.pushButton_6.setText(_translate("MainWindow", "..."))
        self.pushButton_9.setText(_translate("MainWindow", "开始预处理"))
        self.pushButton_8.setText(_translate("MainWindow", "开始训练"))
        self.pushButton_10.setText(_translate("MainWindow", "开始合成"))

    def pre_process(self, state):
        tofig.Video2Figure(self.path_list(), state)
        ExtractTrainingData = extract.ExtractTrainingData(self.path_list())
        ExtractTrainingData.process(state)

    def train_process(self, state):
        train.TrainingProcessor(self.path_list(), state)

    def convert_process(self, state):
        con = convert.ConvertImage(self.path_list(), state)
        con.process()
        if state.empty():
            merge.MergeImage(self, state)
        elif not state.empty():
            if state.get() == 'stop_con':
                path = utils.get_dir(self, 't') + '_convert'
                time.sleep(1)
                if os.path.exists(path):
                    import shutil
                    shutil.rmtree(path)

    def threading_manager(self, cmd):
        global thr_train, thr_convert, thr_preprocess
        if thr_train is None:
            thr_train = threading.Thread(target=self.train_process, args=(state,), kwargs={})
        if thr_convert is None:
            thr_convert = threading.Thread(target=self.convert_process, args=(state,), kwargs={})
        if thr_preprocess is None:
            thr_preprocess = threading.Thread(target=self.pre_process, args=(state,), kwargs={})
        # utils.queue_clear(state)

        if cmd == 'preprocessing':
            if not thr_train.is_alive() and not thr_convert.is_alive():
                try:
                    print('预处理程序启动中……………………')
                    thr_preprocess.setDaemon(True)
                    thr_preprocess.start()
                    return True
                except:
                    thr_preprocess = None
                    self.threading_manager(cmd)
            else:
                self.message('Process Error', '另一个进程正在进行中', '确定')
                return False

        if cmd == 'train':
            if not thr_preprocess.is_alive() and not thr_convert.is_alive():
                try:
                    if not self.dir_check('m'):
                        return False
                    print('训练程序启动中……………………')
                    thr_train.setDaemon(True)
                    thr_train.start()
                    return True
                except:
                    thr_train = None
                    self.threading_manager(cmd)
            else:
                self.message('Process Error', '另一个进程正在进行中', '确定')
                return False

        if cmd == 'convert':
            if not thr_train.is_alive() and not thr_preprocess.is_alive():
                try:
                    if not self.dir_check('c'):
                        return False
                    print('合成程序启动中……………………')
                    thr_convert.setDaemon(True)
                    thr_convert.start()
                    return True
                except:
                    thr_convert = None
                    self.threading_manager(cmd)
            else:
                self.message('Process Error', '另一个进程正在进行中', '确定')
                return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Ui_MainWindow()
    win.show()

    sys.exit(app.exec())

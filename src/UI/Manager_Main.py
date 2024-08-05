# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Manager_Main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 640)
        self.action_add = QAction(MainWindow)
        self.action_add.setObjectName(u"action_add")
        self.action_quit = QAction(MainWindow)
        self.action_quit.setObjectName(u"action_quit")
        self.action_refresh = QAction(MainWindow)
        self.action_refresh.setObjectName(u"action_refresh")
        self.action_modfolder = QAction(MainWindow)
        self.action_modfolder.setObjectName(u"action_modfolder")
        self.action_launchgame = QAction(MainWindow)
        self.action_launchgame.setObjectName(u"action_launchgame")
        self.action_addwithzip = QAction(MainWindow)
        self.action_addwithzip.setObjectName(u"action_addwithzip")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 10, 451, 581))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 480, 22))
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menuBar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.action_add)
        self.menu.addAction(self.action_addwithzip)
        self.menu.addSeparator()
        self.menu.addAction(self.action_quit)
        self.menu_2.addAction(self.action_refresh)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action_modfolder)
        self.menu_2.addAction(self.action_launchgame)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Mini Airways Mod Manager", None))
        self.action_add.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.action_quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.action_refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.action_modfolder.setText(QCoreApplication.translate("MainWindow", u"Open Mod Folder", None))
        self.action_launchgame.setText(QCoreApplication.translate("MainWindow", u"Launch The Game", None))
        self.action_addwithzip.setText(QCoreApplication.translate("MainWindow", u"Open Zip", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"Files", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"Operations", None))
    # retranslateUi


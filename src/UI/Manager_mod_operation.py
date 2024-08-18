# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Manager_mod_operation.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(320, 240)
        Dialog.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 40, 143, 86))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_endisable = QPushButton(self.widget)
        self.pushButton_endisable.setObjectName(u"pushButton_endisable")

        self.verticalLayout_2.addWidget(self.pushButton_endisable)

        self.pushButton_description = QPushButton(self.widget)
        self.pushButton_description.setObjectName(u"pushButton_description")

        self.verticalLayout_2.addWidget(self.pushButton_description)

        self.pushButton_del = QPushButton(self.widget)
        self.pushButton_del.setObjectName(u"pushButton_del")

        self.verticalLayout_2.addWidget(self.pushButton_del)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton_endisable.setText(QCoreApplication.translate("Dialog", u"Enanble/Disable the Mod", None))
        self.pushButton_description.setText(QCoreApplication.translate("Dialog", u"Mod Description", None))
        self.pushButton_del.setText(QCoreApplication.translate("Dialog", u"Delete the Mod", None))
    # retranslateUi


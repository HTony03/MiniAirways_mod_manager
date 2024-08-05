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
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(320, 240)
        self.pushButton_del = QPushButton(Dialog)
        self.pushButton_del.setObjectName(u"pushButton_del")
        self.pushButton_del.setGeometry(QRect(20, 120, 141, 24))
        self.pushButton_endisable = QPushButton(Dialog)
        self.pushButton_endisable.setObjectName(u"pushButton_endisable")
        self.pushButton_endisable.setGeometry(QRect(20, 40, 141, 21))
        self.pushButton_description = QPushButton(Dialog)
        self.pushButton_description.setObjectName(u"pushButton_description")
        self.pushButton_description.setGeometry(QRect(20, 80, 141, 24))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton_del.setText(QCoreApplication.translate("Dialog", u"Delete the Mod", None))
        self.pushButton_endisable.setText(QCoreApplication.translate("Dialog", u"Enanble/Disable the Mod", None))
        self.pushButton_description.setText(QCoreApplication.translate("Dialog", u"Mod Description", None))
    # retranslateUi


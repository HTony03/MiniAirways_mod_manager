import sys

import qdarkstyle
from PySide6 import QtWidgets
from PySide6.QtCore import QTranslator, QLocale
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QCheckBox, QHBoxLayout, QMessageBox, QFileDialog

from src.UI.Main_test import Ui_MainWindow
from src.UI.checkacceptreject import Ui_Dialog as Ui_Dialog_2
from src.UI.dialog_mod_operation import Ui_Dialog

if __name__ == '__main__':
    pass

import os
import platform
import time

import loggerjava as lj

ver = '0.2.5'


# BepInEx folder test
if not os.path.exists('.\\BepInEx\\'):
    app = QApplication([])
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))
    msg_box.setText("""the mod manager is currently not in the Mini Airways Folder
    check your location and open the manager!""")
    msg_box.exec()
    # print('the mod manager is currently not in the Mini Airways Folder')
    # print('check your location and open the manager!')
    sys.exit()

# init log
if not os.path.exists('.\\MiniAirways_mod_manager_log\\'):
    os.mkdir('.\\MiniAirways_mod_manager_log\\')
lj.config(name='.\\MiniAirways_mod_manager_log\\' +
               str(time.gmtime().tm_mon) + '.' + str(time.gmtime().tm_mday) + '_' +
               str(time.gmtime().tm_hour) + '.' + str(time.gmtime().tm_min), showinconsole=False)
lj.clearcurrentlog()
lj.debug('current loggerjava ver:' + lj.ver, pos='test_loggerjava')

mod_database = {}
basemoddic = r'.\BepInEx\plugins\\'
last_refresh = time.time()

from win32com.client import Dispatch
import json

shell = Dispatch("Shell.Application")
# enter directory where your file is located
ns = shell.NameSpace(os.path.abspath(basemoddic))

try:
    def reload_from_disc():
        global mod_database, last_refresh
        mod_database = {}
        name_db = []
        stat_db = []
        have_dumplicates = {}
        ns_list = ns.Items()
        for filename in list(map(lambda x: str(x), ns_list)):
            if os.path.isfile(os.path.join(basemoddic, filename)):
                base, ext = os.path.splitext(filename)
                while ext and base.count('.') > 0:
                    base, new_ext = os.path.splitext(base)
                    ext = new_ext + ext
                index = str(list(map(lambda x: str(x), ns_list)).index(filename))
                if ext == '.dll':
                    filedata = {}
                    for j in [0, 33, 34, 166, 297, 298]:
                        filedata[ns.GetDetailsOf(j, j)] = ns.GetDetailsOf(
                            list(ns.Items())[list(map(lambda x: str(x), ns_list)).index(filename)], j)
                    lj.info('read filedata(%s):' % index + str(filedata), pos='disc_load_thread')
                    if filedata["File description"] not in name_db:
                        mod_database['mod' + str(len(mod_database))] = {
                            "name": filedata["File description"],
                            "file_name": base + '.dll',
                            'ver': filedata["File version"],
                            "active": "True"
                        }
                        name_db.append(filedata["File description"])
                        stat_db.append(1)

                    else:
                        # test ver

                        enablestat = 0
                        dumplicate_index = []
                        dumplicate_ver = []
                        for i in range(len(stat_db)):
                            if name_db[i] == filedata["File description"]:
                                enablestat += stat_db[i]
                                if stat_db[i]:
                                    dumplicate_index.append(i)
                                    dumplicate_ver.append(mod_database['mod' + str(i)]['ver'])
                        dumplicate_index.append(len(mod_database))
                        dumplicate_ver.append(filedata["File version"])
                        lj.info('handling dumplicate:' + str({
                            'index': dumplicate_index,
                            'ver': dumplicate_ver
                        }), pos='disc_load_thread')
                        if enablestat:
                            have_dumplicates[filedata["File description"]] = {
                                'index': dumplicate_index,
                                'ver': dumplicate_ver
                            }

                        mod_database['mod' + str(len(mod_database))] = {
                            "name": filedata["File description"],
                            "file_name": base + '.dll',
                            'ver': filedata["File version"],
                            "active": "True"
                        }
                        name_db.append(filedata["File description"])
                        stat_db.append(1)


                elif ext == '.dll.disabled':
                    changed_name = None
                    try:
                        os.rename(os.path.join(basemoddic, filename), os.path.join(basemoddic, base + '.dll'))
                        changed_name = os.path.join(basemoddic, base + '.dll')
                    except FileExistsError:
                        file_name_add = list(range(1, 11)) + ['a', 'b']
                        for addname in range(len(file_name_add)):
                            if not os.path.exists(os.path.join(basemoddic, base + '_%s.dll' % file_name_add[addname])):
                                os.rename(os.path.join(basemoddic, filename), os.path.join(basemoddic, base +
                                                                                           '_%s.dll' %
                                                                                           file_name_add[addname]))
                                changed_name = os.path.join(basemoddic, base + '_%s.dll' % file_name_add[addname])
                                break
                    if not changed_name:
                        lj.info('hmmmm what do you want do to XD\nskipping the file', pos='disc_load_thread')
                        continue
                    filedata = {}
                    # for j in range(0, 321): if (ns.GetDetailsOf(list(ns.Items())[list(map(lambda x:str(x),
                    # ns_list)).index(filename)], j) and ns.GetDetailsOf(j, j) in ['Name', 'File description',
                    # 'Company', 'File version', 'Product name', 'Product version'] \ ): filedata[ns.GetDetailsOf(j,
                    # j)] = ns.GetDetailsOf(list(ns.Items())[list(map(lambda x:str(x),ns_list)).index(filename)], j)
                    for j in [0, 33, 34, 166, 297, 298]:
                        filedata[ns.GetDetailsOf(j, j)] = ns.GetDetailsOf(
                            list(ns.Items())[list(map(lambda x: str(x), ns_list)).index(filename)], j)
                    lj.info('read filedata(%s):' % index + str(filedata), pos='disc_load_thread')
                    mod_database['mod' + str(len(mod_database))] = {
                        "name": filedata["File description"],
                        "file_name": base + '.dll',
                        'ver': filedata["File version"],
                        "active": "False"
                    }
                    name_db.append(filedata["File description"])
                    stat_db.append(0)
                    os.rename(changed_name, os.path.join(basemoddic, filename))
        last_refresh = time.time()

        # handle dumplicates
        lj.warn('dumplicates:' + str(have_dumplicates), pos='disc_load_thread')
        for name, val in have_dumplicates.items():
            vern = val['ver']
            indexn = val['index']
            max_ver = max(vern)
            max_ver_index = indexn[vern.index(max_ver)]
            indexn.remove(max_ver_index)
            vern.remove(max_ver)
            for indexs in indexn:
                os.rename(os.path.join(basemoddic, mod_database['mod' + str(indexs)]['file_name']),
                          os.path.join(basemoddic, mod_database['mod' + str(indexs)]['file_name'] + '.disabled'))
                mod_database['mod' + str(indexs)]['active'] = "False"

        lj.info("loaded mods from disc!", pos='disc_load_thread')


    def delmod(index):
        global mod_database
        filedir = mod_database['mod' + str(index)]['file_name']
        dll_file_path = r'.\BepInEx\plugins\\' + filedir
        if os.path.exists(dll_file_path):
            os.remove(dll_file_path)
            lj.info(f"Mod file file %s has been deleted." % dll_file_path)
        elif os.path.exists(dll_file_path + ".disabled"):
            os.remove(dll_file_path + ".disabled")
            lj.info(f"Mod file file %s.disabled has been deleted." % dll_file_path)
        else:
            lj.info(f"Mod file %s does not exist.\n" % dll_file_path +
                    f"removing the related mod data")
        lj.info('deleting mod with index %s' % index)
        lj.info("deleted!")
        Mainwindow.refresh_data()

    # TODO: refresh to another thread(auto refresh)
    # TODO: performance improvements
    def enablemod(index):
        # TODO: check whether have dumplicate mods enabled(先两个后多个compact)
        global mod_database
        filedir = mod_database['mod' + str(index)]['file_name']

        if mod_database['mod' + str(index)]['active'] != "False":
            lj.info(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal(not active)\n"
                                                                    "aborting and refreshing... ")
            Mainwindow.refresh_data()
            return
        if not os.path.exists(basemoddic + filedir + '.disabled'):
            lj.info(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal(no file)\n"
                                                                    "aborting and refreshing... ")
            mod_database['mod' + str(index)]['active'] = "False"
            Mainwindow.refresh_data()
            return
        os.rename(basemoddic + filedir + '.disabled', basemoddic + filedir)
        mod_database['mod' + str(index)]['active'] = "True"
        lj.info("changed mod " + mod_database['mod' + str(index)]['name'] + ' status to enabled')


    def disablemod(index):
        global mod_database
        filedir = mod_database['mod' + str(index)]['file_name']

        if mod_database['mod' + str(index)]['active'] != "True":
            lj.info(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal(not deactive)\n"
                                                                    "aborting and refreshing... ")
            Mainwindow.refresh_data()
            return
        if not os.path.exists(basemoddic + filedir):
            lj.info(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnorma(no file)l\n"
                                                                    "aborting and refreshing... ")
            mod_database['mod' + str(index)]['active'] = "False"
            Mainwindow.refresh_data()
            return
        os.rename(basemoddic + filedir, basemoddic + filedir + '.disabled')
        mod_database['mod' + str(index)]['active'] = "False"
        lj.info('disabling mod with index %s' % index)
        lj.info("changed mod " + mod_database['mod' + str(index)]['name'] + ' status to disabled')

    def launchgame():
        os.popen(r'MiniAirways.exe')

    def openmodfolder():
        os.system('explorer ' + os.path.abspath(basemoddic))


    lj.register_def(reload_from_disc)
    lj.register_def(delmod)
    lj.register_def(enablemod)
    lj.register_def(disablemod)
    lj.register_def(launchgame)
    lj.register_def(openmodfolder)

    if __name__ == '__main__':
        pass

    lj.info('Mini Airways Mod manager %s on %s' % (ver, platform.system()))
    lj.info('init ui...')


    class ModMannager_MainUI(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            global data
            lj.info('showing MainUI',pos='Ui_MainUI')
            data = mod_database

            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.action_refresh.triggered.connect(self.refresh_data)
            self.ui.action_quit.triggered.connect(self.close)
            self.ui.action_add.triggered.connect(self.addFile)
            self.ui.action_modfolder.triggered.connect(openmodfolder)
            self.ui.action_launchgame.triggered.connect(launchgame)
            self.setWindowIcon(QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))

            self.refresh_data()

            self.show()

        def refresh_data(self):
            # Call the outer function that refreshes the data
            lj.info('refresh data called',pos='Ui_MainUI')
            reload_from_disc()
            global data
            data = mod_database
            # Update the UI accordingly
            self.update_ui()

        def update_ui(self):
            lj.info('refreshing ui',pos='Ui_MainUI')
            global data
            data = mod_database
            # Code to update the UI based on the refreshed data
            self.ui.tableWidget.setRowCount(0)

            self.ui.tableWidget.setRowCount(len(data))  # Set the number of rows
            self.ui.tableWidget.setColumnCount(4)  # Set the number of columns
            # self.ui.tableWidget.setSortingEnabled(True)
            namedb = []
            for i in range(len(data)):
                namedb.append(data['mod' + str(i)]['name'])
            self.ui.tableWidget.setColumnWidth(0, max(map(lambda x: len(x), namedb + ['name'])) * 8)
            self.ui.tableWidget.setColumnWidth(1, 70)
            self.ui.tableWidget.setColumnWidth(2, 50)
            self.ui.tableWidget.setColumnWidth(3, 100)

            self.ui.tableWidget.setHorizontalHeaderLabels(['mod', '版本', '状态', '操作'])
            for i, row in enumerate(data):
                # self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i+1)))
                self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(data[row]['name']))
                self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(data[row]['ver']))
                # self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(data[row]['active']))
                checkbox = QCheckBox(self)
                if data[row]['active'] == 'True':
                    checkbox.setChecked(True)
                else:
                    checkbox.setChecked(False)
                checkbox.stateChanged.connect(lambda state, row=i: self.handleCheckboxStateChange(state, row))
                # Create a QWidget as a container for the checkbox
                widget = QWidget()
                # Create a QHBoxLayout
                layout = QHBoxLayout(widget)
                # Add the checkbox to the layout
                layout.addWidget(checkbox)
                # Align the checkbox to the center
                layout.setAlignment(Qt.AlignCenter)
                # Remove the margins
                layout.setContentsMargins(0, 0, 0, 0)
                widget.setLayout(layout)

                button = QtWidgets.QPushButton('操作')
                button.clicked.connect(
                    lambda checked, row=i: Op_OperationUi(row))

                self.ui.tableWidget.setCellWidget(i, 2, widget)
                self.ui.tableWidget.setCellWidget(i, 3, button)  # Set the button as the cell widget

            self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        def addFile(self):

            # Create a file dialog
            file_dialog = QFileDialog()

            # Set the file dialog to open in file selection mode
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Application extension (*.dll)")
            file_dialog.show()

            # Show the file dialog and get the selected file(s)
            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                # print(selected_files)
            lj.info('adding a mod with route:%s'%selected_files,pos='Ui_MainUI')
            os.system('copy "%s" "%s"' % (selected_files[0], os.path.join(basemoddic ,
                                                                        os.path.basename(selected_files[0]))))
            self.refresh_data()


        def addFile_zip(self):
            # Create a file dialog
            file_dialog = QFileDialog()

            # Set the file dialog to open in file selection mode
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Zip file (*.zip)")
            file_dialog.show()

            # Show the file dialog and get the selected file(s)
            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                print(selected_files)
                # os.system('copy "%s" %s' % (selected_files[0], basemoddic + os.path.basename(selected_files[0])))
                self.refresh_data()

        def handleCheckboxStateChange(self, state, index):
            if state == 2:
                enablemod(index)
            elif state == 0:
                disablemod(index)


    class OperationUi(QtWidgets.QDialog):
        def __init__(self, index):
            super().__init__()
            lj.info('showing OperationUi with index %s'%index,pos='Ui_OperationUi')
            self.ui = Ui_Dialog()
            self.ui.setupUi(self)
            self.ui.pushButton_del.clicked.connect(
                lambda checked: self.handle(index))
            self.setWindowIcon(QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))

            self.show()

        def handle(self, index):
            self.close()
            Op_ConfirmUi(index, '确认删除?', {'confirm':'delmod(self.index)'})


    class ConfirmUi(QtWidgets.QDialog):
        def __init__(self, index, text, operation):
            super().__init__()
            lj.info('showing ConfirmUi with keys: (%s,%s,%s)' % (index,text,operation), pos='Ui_ConfirmUi')
            self.operation = operation
            self.index = index
            self.ui = Ui_Dialog_2()
            self.ui.setupUi(self)
            self.ui.textBrowser.setText(text)
            self.setWindowIcon(QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))
            self.show()

        def accept(self):
            self.done(1)
            if 'confirm' in self.operation:
                exec(self.operation['confirm'])


        def reject(self):
            self.done(0)
            if 'reject' in self.operation:
                exec(self.operation['confirm'])


    def Op_OperationUi(index):
        Operationwindow = OperationUi(index)
        Operationwindow.exec()


    def Op_ConfirmUi(index, text,operation):
        Confirmwindow = ConfirmUi(index, text,operation)
        Confirmwindow.exec()


    def load_translator(app, locale):
        translator = QTranslator(app)

        # Load the appropriate .qm file based on the locale
        if locale.language() == QLocale.Chinese:
            translator.load("translations/chinese.qm")
        elif locale.language() == QLocale.English:
            translator.load("translations/english.qm")
        else:
            # Default to English if the locale is not supported
            translator.load("translations/english.qm")

    lj.register_def(ModMannager_MainUI)
    lj.register_def(ConfirmUi)
    lj.register_def(OperationUi)
    lj.register_def(Op_OperationUi)
    lj.register_def(Op_ConfirmUi)
    lj.register_def(load_translator)


    # TODO:add through zip files

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        translator = QTranslator(app)
        translator.load("Main_test.qm")
        app.installTranslator(translator)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
        Mainwindow = ModMannager_MainUI()
        sys.exit(app.exec())
except Exception as E:
    lj.warn(lj.handler(E), pos='exechandler', showinconsole=True)
    lj.info('db:\n' + json.dumps(mod_database, ensure_ascii=True, indent=4, sort_keys=False), pos='exechandler')
    lj.info('ver: %s os: %s' % (ver, platform.system()), pos='exechandler')
    app = QApplication([])
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))
    msg_box.setText("""please upload the latest log after the whole program is exited(after the console is closed).')
the log is in 'MiniAirways_mod_manager_log' folder.""")
    msg_box.exec()
    sys.exit()

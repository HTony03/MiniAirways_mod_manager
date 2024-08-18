import shutil
import sys
import zipfile

import qdarkstyle
from PySide6 import QtWidgets
from PySide6.QtCore import QTranslator, QLocale
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QCheckBox, QHBoxLayout, QMessageBox, QFileDialog
from PySide6.QtGui import QKeySequence, QShortcut

from src.UI.Manager_Main import Ui_MainWindow
from src.UI.Manager_check_yn import Ui_Dialog as Dialog_check_yn
from src.UI.Manager_mod_operation import Ui_Dialog as Dialog_mod_operation

if __name__ == '__main__':
    pass

import os
import platform
import time

import loggerjava as lj

ver = '0.2.7'

# BepInEx folder test
if not os.path.exists('.\\BepInEx\\'):
    app = QApplication([])
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))
    msg_box.setText("""the mod manager is currently not in the Mini Airways Folder
    check your location and open the manager!""")
    msg_box.exec()
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
in_lang = {}
basemoddic = r'.\BepInEx\plugins\\'
last_refresh = time.time()

from win32com.client import Dispatch
import json

shell = Dispatch("Shell.Application")
# enter directory where your file is located
ns = shell.NameSpace(os.path.abspath(basemoddic))

try:
    def reload_from_disc(Mainwindow):
        global mod_database, last_refresh
        mod_database = {}
        name_db = []
        stat_db = []
        have_dumplicates = {}
        ns_list = ns.Items()
        index_now = 0
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
            index_now += 1
            Mainwindow.update_ui(int(index_now / len(ns_list)))
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
        dll_file_path = basemoddic + filedir
        if os.path.exists(dll_file_path):
            os.remove(dll_file_path)
            mod_database.pop('mod' + str(index))
            lj.info(f"Mod file file %s has been deleted." % dll_file_path)
        elif os.path.exists(dll_file_path + ".disabled"):
            os.remove(dll_file_path + ".disabled")
            mod_database.pop('mod' + str(index))
            lj.info(f"Mod file file %s.disabled has been deleted." % dll_file_path)
        else:
            lj.info(f"Mod file %s does not exist.\n" % dll_file_path +
                    f"removing the related mod data")
            mod_database.pop('mod' + str(index))
        lj.info('deleting mod with index %s' % index)
        lj.info("deleted!")
        Mainwindow.refresh_data()


    # TODO: refresh to another thread(auto refresh)
    # TODO: performance improvements


    def enablemod(index):
        global mod_database
        lj.info('try enabling mod index %s' % index)

        mod_name = mod_database['mod' + str(index)]['name']
        mod_ver = mod_database['mod' + str(index)]['ver']
        dumplicate_index = []
        dumplicate_ver = []
        value = mod_database.values()
        for i in range(len(mod_database)):
            if list(value)[i]['name'] == mod_name and i != index and list(value)[i]['active'] == 'True':
                dumplicate_index.append(i)
                dumplicate_ver.append(list(value)[i]['ver'])
        if dumplicate_ver:
            lj.warn('dumplicates!%s' % dumplicate_index)
            if mod_ver <= max(dumplicate_ver):
                msg_box = QMessageBox()
                msg_box.setWindowIcon(
                    QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))
                msg_box.setText(in_lang['warn.dumplicate_mod_higher_ver'])
                msg_box.exec()
                Mainwindow.update_ui()
                return

            for d_index in dumplicate_index:
                disablemod(d_index)
                Mainwindow.update_ui()

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
        Mainwindow.update_ui()


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
        Mainwindow.update_ui()


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
            lj.info('showing MainUI', pos='Ui_MainUI')

            self.shortcut = QShortcut(QKeySequence("F5"), self)
            # Connect the activated signal of the shortcut to the reload_from_disc function
            self.shortcut.activated.connect(self.refresh_data)


            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.action_refresh.triggered.connect(self.refresh_data)
            self.ui.action_quit.triggered.connect(self.close)
            self.ui.action_add.triggered.connect(self.addFile)
            self.ui.action_addwithzip.triggered.connect(self.addFile_zip)
            self.ui.action_modfolder.triggered.connect(openmodfolder)
            self.ui.action_launchgame.triggered.connect(launchgame)
            self.setWindowIcon(QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))

            self.refresh_data()

            self.show()

        def refresh_data(self):
            # Call the outer function that refreshes the data
            lj.info('refresh data called', pos='Ui_MainUI')
            reload_from_disc(self)
            # Update the UI accordingly
            self.update_ui()

        def update_ui(self, progress:int=100):
            lj.info('refreshing ui', pos='Ui_MainUI')
            # Code to update the UI based on the refreshed data
            self.ui.tableWidget.setRowCount(0)

            self.ui.tableWidget.setRowCount(len(mod_database))  # Set the number of rows
            self.ui.tableWidget.setColumnCount(4)  # Set the number of columns
            # self.ui.tableWidget.setSortingEnabled(True)
            namedb = []
            for i in range(len(mod_database)):
                namedb.append(mod_database['mod' + str(i)]['name'])
            self.ui.tableWidget.setColumnWidth(0, max(max(map(lambda x: len(x), namedb + ['name'])), 24) * 7)
            self.ui.tableWidget.setColumnWidth(1, 70)
            self.ui.tableWidget.setColumnWidth(2, 50)
            self.ui.tableWidget.setColumnWidth(3, 100)
            self.ui.progressBar.setValue(progress)

            self.ui.tableWidget.setHorizontalHeaderLabels([in_lang['label.0'], in_lang['label.1'],
                                                           in_lang['label.2'], in_lang['label.3']])
            for i, row in enumerate(mod_database):
                self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(mod_database[row]['name']))
                self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(mod_database[row]['ver']))
                checkbox = QCheckBox(self)
                if mod_database[row]['active'] == 'True':
                    checkbox.setChecked(True)
                else:
                    checkbox.setChecked(False)
                checkbox.stateChanged.connect(lambda state, index=i: self.handleCheckboxStateChange(state, index))
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

                button = QtWidgets.QPushButton(in_lang['Operation.operation'])
                button.clicked.connect(
                    lambda checked, index=i: Op_OperationUi(index))

                self.ui.tableWidget.setCellWidget(i, 2, widget)
                self.ui.tableWidget.setCellWidget(i, 3, button)  # Set the button as the cell widget

            self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        def addFile(self):

            # Create a file dialog
            file_dialog = QFileDialog()

            # Set the file dialog to open in file selection mode
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Application extension (*.dll)")
            file_dialog.setWindowIcon(QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))
            file_dialog.show()

            # Show the file dialog and get the selected file(s)
            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                # print(selected_files)
                lj.info('adding a mod with route:%s' % selected_files, pos='Ui_MainUI')
                os.system('copy "%s" "%s"' % (selected_files[0], os.path.join(basemoddic,
                                                                              os.path.basename(selected_files[0]))))
                self.refresh_data()

        def addFile_zip(self):
            # Create a file dialog
            file_dialog = QFileDialog()

            # Set the file dialog to open in file selection mode
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Zip file (*.zip)")
            file_dialog.setWindowIcon(QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))
            file_dialog.show()

            # Show the file dialog and get the selected file(s)
            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                with zipfile.ZipFile(selected_files[0], 'r', metadata_encoding='gbk') as zip_ref:
                    for file_info in zip_ref.infolist():
                        base, ext = os.path.splitext(file_info.filename)
                        while ext and base.count('.') > 0:
                            base, new_ext = os.path.splitext(base)
                            ext = new_ext + ext
                        if ext == '.dll':
                            zip_ref.extract(file_info, path=basemoddic)
                            if len(base.split('/')) == 2:
                                shutil.copy(os.path.join(basemoddic, base + ext),
                                            os.path.join(basemoddic, base.split('/')[1] + ext))
                                shutil.rmtree(os.path.join(basemoddic, base.split('/')[0]))

                # os.system('copy "%s" %s' % (selected_files[0], basemoddic + os.path.basename(selected_files[0])))
                self.refresh_data()

        def handleCheckboxStateChange(self, state, index):
            if state == 2:
                enablemod(index)
            elif state == 0:
                disablemod(index)

        def setprogressbarvalue(self, progress:int):
            self.ui.progressBar.value(progress)




    class OperationUi(QtWidgets.QDialog):
        def __init__(self, index):
            super().__init__()
            lj.info('showing OperationUi with index %s' % index, pos='Ui_OperationUi')
            self.ui = Dialog_mod_operation()
            self.ui.setupUi(self)
            self.ui.pushButton_del.clicked.connect(
                lambda checked: self.handle_del(index)
            )
            self.ui.pushButton_endisable.clicked.connect(
                lambda checked: self.handle_stat_change(index)
            )
            self.setWindowIcon(QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))

            self.show()

        def handle_del(self, index):
            self.close()
            Op_ConfirmUi(index, in_lang['Operation.Confirmdel'], {'confirm': 'delmod(self.index)'})

        def handle_stat_change(self, index):
            self.close()
            if mod_database['mod' + str(index)]['active'] == 'True':
                disablemod(index)
            else:
                enablemod(index)


    class ConfirmUi(QtWidgets.QDialog):
        def __init__(self, index, text, operation):
            super().__init__()
            lj.info('showing ConfirmUi with keys: (%s,%s,%s)' % (index, text, operation), pos='Ui_ConfirmUi')
            self.operation = operation
            self.index = index
            self.ui = Dialog_check_yn()
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


    def Op_ConfirmUi(index, text, operation):
        Confirmwindow = ConfirmUi(index, text, operation)
        Confirmwindow.exec()


    def load_translator():
        global translator, in_lang

        # Load the appropriate .qm file based on the locale
        if QLocale.Language() == QLocale.Language.Chinese:
            translator.load(r'.\Ui\Main_zh_CN.qm')
            in_lang = {
                'Operation.Confirmdel': '确认删除?',
                'Operation.operation': '操作',
                'label.0': 'Mod',
                'label.1': '版本',
                'label.2': '状态',
                'label.3': '操作',
                'warn.dumplicate_mod_higher_ver': '更高或相同版本的同Mod处在启用状态！'
            }
        # elif QLocale.Language() == QLocale.Language.AnyLanguage:
        #     translator.load(r'.\Ui\Main_zh_CN.qm')
        elif QLocale.Language() == QLocale.Language.English:
            in_lang = {
                'Operation.Confirmdel': 'Confirm deletion?',
                'Operation.operation': 'Operation',
                'label.0': 'Mod',
                'label.1': 'Version',
                'label.2': 'Status',
                'label.3': 'Operation',
                'warn.dumplicate_mod_higher_ver': '''The same mod with a higher or same version is in active mode!
                                Aborting'''
            }
        else:
            # Default to English if the locale is not supported
            in_lang = {
                'Operation.Confirmdel': 'Confirm deletion?',
                'Operation.operation': 'Operation',
                'label.0': 'Mod',
                'label.1': 'Version',
                'label.2': 'Status',
                'label.3': 'Operation',
                'warn.dumplicate_mod_higher_ver': '''The same mod with a higher or same version is in active mode!
                                Aborting'''
            }


    lj.register_def(ModMannager_MainUI)
    lj.register_def(ConfirmUi)
    lj.register_def(OperationUi)
    lj.register_def(Op_OperationUi)
    lj.register_def(Op_ConfirmUi)
    lj.register_def(load_translator)

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        translator = QTranslator(app)
        # print(QLocale.system().Language)
        # translator.load(r'.\Ui\Main_zh_CN.qm')
        # # translator.load(r'.\Ui\Manager_Main.qm')
        # print(translator.filePath())
        # print(translator.language())
        # print(translator.translate('Dialog','Dialog'))
        load_translator()
        app.installTranslator(translator)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
        Mainwindow = ModMannager_MainUI()
        sys.exit(app.exec())
except Exception as E:
    lj.warn(lj.handler(E), pos='exechandler', showinconsole=True)
    lj.info('db:\n' + json.dumps(mod_database, ensure_ascii=True, indent=4, sort_keys=False), pos='exechandler')
    lj.info('ver: %s os: %s' % (ver, platform.system()), pos='exechandler')
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'))
    msg_box.setText("""please upload the latest log after the whole program is exited\n(after the window is closed).
the log is in 'MiniAirways_mod_manager_log' folder.""")
    msg_box.exec()
    sys.exit()

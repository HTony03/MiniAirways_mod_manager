import shutil
import sys
import zipfile
import os
import platform
import datetime
import threading
import send2trash

import qdarkstyle
from PySide6 import QtWidgets
from PySide6.QtCore import QTranslator, QLocale, Qt, Signal
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QWidget, QCheckBox, QHBoxLayout, QMessageBox, QFileDialog

from src.UI.Manager_Main import Ui_MainWindow
from src.UI.Manager_check_yn import Ui_Dialog as Dialog_check_yn
from src.UI.Manager_mod_operation import Ui_Dialog as Dialog_mod_operation

from loguru import logger as lj
import traceback

ver = '0.3.0.dev1'
stop_event = threading.Event()
ICONPATH = r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways\MiniAirways.ico'

# BepInEx folder test
if not os.path.exists('.\\BepInEx\\') or not os.path.exists('.\\BepInEx\\plugins\\'):
    lj.error('BepInEx folder not found'+', pos='+'init')
    app = QApplication([])
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(ICONPATH))
    msg_box.setText("""the mod manager is currently not in the Mini Airways Mod branch Folder
    check your location, steam game branch settings and open the manager again!""")
    msg_box.exec()
    sys.exit()

# init log
if not os.path.exists('.\\MiniAirways_mod_manager_log\\'):
    os.mkdir('.\\MiniAirways_mod_manager_log\\')
lj.add('.\\MiniAirways_mod_manager_log\\miniairways_mod_manager_' + datetime.datetime.now().strftime('%Y%m%d_%H.%M.%S') + '.log', 
       format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> |'
       '<level>{level: <8}</level> |'
       '<cyan>{function}</cyan> -'
       '<level>{message}</level>')

mod_database = {}
in_lang = {}
basemoddic = r'.\BepInEx\plugins\\'
last_refresh = datetime.datetime.now().timestamp()

from win32com.client import Dispatch

shell = Dispatch("Shell.Application")
# enter directory where your file is located
ns = shell.NameSpace(os.path.abspath(basemoddic))

attribute_indices = {
    "Name": 0,
    "File description": 33,
    "Company": 34,
    "File version": 166,
    "Product name": 297,
    "Product version": 298
}

def reload_from_disc(Mainwindow):
    global mod_database, last_refresh
    mod_database = {}
    name_db = []
    stat_db = []
    have_dumplicates = {}
    if not ns:
        lj.error('plugins folder not found'+', pos='+'disc_load_thread')
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(ICONPATH))
        msg_box.setText("""the mod manager is currently not in the Mini Airways Mod branch Folder
        check your location, steam game branch settings and open the manager again!""")
        msg_box.exec()
        sys.exit()
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
                for attr, idx in attribute_indices.items():
                    filedata[attr] = ns.GetDetailsOf(list(ns.Items())[list(map(lambda x: str(x), ns_list)).index(filename)], idx)
                lj.info('read filedata(%s):' % index + str(filedata)+', pos='+'disc_load_thread')
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
                    })+', pos='+'disc_load_thread')
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
                    for adds in ['']+list(range(1,10))+['a','b']:
                        if not os.path.exists(os.path.join(basemoddic, base + f'{adds}.dll')):
                            os.rename(os.path.join(basemoddic, filename), os.path.join(basemoddic, base + f'{adds}.dll'))
                            changed_name = os.path.join(basemoddic, base + f'{adds}.dll')
                            break
                    else:
                        changed_name = None
                except Exception as E:
                    changed_name = None
                    msg_box = QMessageBox()
                    msg_box.setWindowIcon(QIcon(ICONPATH))
                    msg_box.setText("""Failed to refresh the mod, please check whether the application is running in administrator mode and try to restart the program!""")
               
                if not changed_name:
                    lj.info('hmmmm what do you want do to XD\nskipping the file'+', pos='+'disc_load_thread')
                    continue
                filedata = {}
                for attr, idx in attribute_indices.items():
                    filedata[attr] = ns.GetDetailsOf(list(ns.Items())[list(map(lambda x: str(x), ns_list)).index(filename)], idx)
                lj.info('read filedata(%s):' % index + str(filedata)+', pos='+'disc_load_thread')
                mod_database['mod' + str(len(mod_database))] = {
                    "name": filedata["File description"],
                    "file_name": base + '.dll',
                    'ver': filedata["File version"],
                    "active": "False"
                }
                name_db.append(filedata["File description"])
                stat_db.append(0)
                try:
                    os.rename(changed_name, os.path.join(basemoddic, filename))
                except Exception as E:
                    msg_box = QMessageBox()
                    msg_box.setWindowIcon(QIcon(ICONPATH))
                    msg_box.setText("""Failed to refresh the mod, please check whether the application is running in administrator mode and try to restart the program!""")
               
        index_now += 1
        Mainwindow.setprogressbarvalue(int(index_now / len(ns_list) * 100))
    last_refresh = datetime.datetime.now().timestamp()
    lj.warning('dumplicates:' + str(have_dumplicates)+', pos='+'disc_load_thread')
    for name, val in have_dumplicates.items():
        vern = val['ver']
        indexn = val['index']
        max_ver = max(vern)
        max_ver_index = indexn[vern.index(max_ver)]
        indexn.remove(max_ver_index)
        vern.remove(max_ver)
        try:
            for indexs in indexn:
                os.rename(os.path.join(basemoddic, mod_database['mod' + str(indexs)]['file_name']),
                        os.path.join(basemoddic, mod_database['mod' + str(indexs)]['file_name'] + '.disabled'))
                mod_database['mod' + str(indexs)]['active'] = "False"
        except Exception as E:
            msg_box = QMessageBox()
            msg_box.setWindowIcon(QIcon(ICONPATH))
            msg_box.setText("""Failed to refresh the mod, please check whether the application is running in administrator mode and try to restart the program!""")
               
    lj.info("loaded mods from disc!"+', pos='+'disc_load_thread')

def delmod(index):
    global mod_database
    lj.info('deling mod with index %s' % index)
    filedir = mod_database['mod' + str(index)]['file_name']
    dll_file_path = os.path.join(basemoddic, filedir)
    try:
        if os.path.exists(dll_file_path):
            send2trash.send2trash(dll_file_path)
            mod_database.pop('mod' + str(index))
            lj.info(f"Mod file {dll_file_path} has been deleted.")
        elif os.path.exists(dll_file_path + ".disabled"):
            send2trash.send2trash(dll_file_path + ".disabled")
            mod_database.pop('mod' + str(index))
            lj.info(f"Mod file {dll_file_path}.disabled has been deleted.")
        else:
            lj.info(f"Mod file {dll_file_path} does not exist.\n" +
                    f"removing the related mod data")
            mod_database.pop('mod' + str(index))
        lj.info('deleting mod with index %s' % index)
        lj.info("deleted!")
        Mainwindow.refresh_data()
    except Exception as E:
        lj.error(traceback.format_exc())
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(ICONPATH))
        msg_box.setText("""Failed to move the file to the recycle bin, please check whether the application is running in administrator mode and try to restart the program!""")

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
        lj.warning('dumplicates!%s' % dumplicate_index)
        if mod_ver <= max(dumplicate_ver):
            msg_box = QMessageBox()
            msg_box.setWindowIcon(QIcon(ICONPATH))
            msg_box.setText(in_lang['warning.dumplicate_mod_higher_ver'])
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
    if not os.path.exists(os.path.join(basemoddic, filedir + '.disabled')):
        lj.info(
            'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal(no file)\n"
                                                                "aborting and refreshing... ")
        mod_database['mod' + str(index)]['active'] = "False"
        Mainwindow.refresh_data()
        return
    try:
        os.rename(os.path.join(basemoddic, filedir + '.disabled'), os.path.join(basemoddic, filedir))
        mod_database['mod' + str(index)]['active'] = "True"
        lj.info("changed mod " + mod_database['mod' + str(index)]['name'] + ' status to enabled')
        Mainwindow.update_ui()
    except Exception as E:
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(ICONPATH))
        msg_box.setText("""Failed to active the mod, please check whether the application is running in administrator mode and try to restart the program!""")
# TODO: convert into one:modestatchange(operation:'active')
def disablemod(index):
    global mod_database
    filedir = mod_database['mod' + str(index)]['file_name']

    if mod_database['mod' + str(index)]['active'] != "True":
        lj.info(
            'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal(not deactive)\n"
                                                                "aborting and refreshing... ")
        Mainwindow.refresh_data()
        return
    if not os.path.exists(os.path.join(basemoddic, filedir)):
        lj.info(
            'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnorma(no file)l\n"
                                                                "aborting and refreshing... ")
        mod_database['mod' + str(index)]['active'] = "False"
        Mainwindow.refresh_data()
        return
    try:
        os.rename(os.path.join(basemoddic, filedir), os.path.join(basemoddic, filedir + '.disabled'))
        mod_database['mod' + str(index)]['active'] = "False"
        lj.info('disabling mod with index %s' % index)
        lj.info("changed mod " + mod_database['mod' + str(index)]['name'] + ' status to disabled')
        Mainwindow.update_ui()
    except Exception as E:
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(ICONPATH))
        msg_box.setText("""Failed to disable the mod, please check whether the application is running in administrator mode and try to restart the program!""")

def launchgame():
    os.popen(r'MiniAirways.exe')

def openmodfolder():
    os.system('explorer ' + os.path.abspath(basemoddic))



# Start the auto-refresh thread


class ModMannager_MainUI(QtWidgets.QMainWindow):
    refresh_signal = Signal()
    
    def __init__(self):
        super().__init__()
        global refresh
        lj.info('showing MainUI'+', pos='+'Ui_MainUI')

        self.shortcut = QShortcut(QKeySequence("F5"), self)
        self.shortcut.activated.connect(self.refresh_data)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.action_refresh.triggered.connect(self.refresh_data)
        self.ui.action_quit.triggered.connect(self.closeEvent)
        self.ui.action_add.triggered.connect(self.addFile)
        self.ui.action_addwithzip.triggered.connect(self.addFile_zip)
        self.ui.action_modfolder.triggered.connect(openmodfolder)
        self.ui.action_launchgame.triggered.connect(launchgame)
        self.setWindowIcon(QIcon(ICONPATH))

        self.refresh_data()
        refresh = threading.Thread(target=self.auto_refresh)
        refresh.start()
        lj.info('started thread')

        self.show()

        # Connect the signal to the refresh_data method
        self.refresh_signal.connect(self.refresh_data)

    def refresh_data(self):
        lj.info('refresh data called'+', pos='+'Ui_MainUI')
        reload_from_disc(self)
        self.update_ui()

    def update_ui(self):
        lj.info('refreshing ui'+', pos='+'Ui_MainUI')
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setRowCount(len(mod_database))
        self.ui.tableWidget.setColumnCount(4)
        namedb = [mod_database['mod' + str(i)]['name'] for i in range(len(mod_database))]
        self.ui.tableWidget.setColumnWidth(0, max(max(map(lambda x: len(x), namedb + ['name'])), 24) * 7)
        self.ui.tableWidget.setColumnWidth(1, 70)
        self.ui.tableWidget.setColumnWidth(2, 50)
        self.ui.tableWidget.setColumnWidth(3, 100)
        self.ui.tableWidget.setHorizontalHeaderLabels([in_lang['label.0'], in_lang['label.1'],
                                                       in_lang['label.2'], in_lang['label.3']])
        for i, row in enumerate(mod_database):
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(mod_database[row]['name']))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(mod_database[row]['ver']))
            checkbox = QCheckBox(self)
            checkbox.setChecked(mod_database[row]['active'] == 'True')
            checkbox.stateChanged.connect(lambda state, index=i: self.handleCheckboxStateChange(state, index))
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(layout)
            button = QtWidgets.QPushButton(in_lang['Operation.operation'])
            button.clicked.connect(lambda checked, index=i: Op_OperationUi(index))
            self.ui.tableWidget.setCellWidget(i, 2, widget)
            self.ui.tableWidget.setCellWidget(i, 3, button)
        self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

    def addFile(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setWindowIcon(QIcon(ICONPATH))
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', filter="Application extension (*.dll)")
        if file[0]:
            lj.info('adding a mod with route:%s' % file[0]+', pos='+'Ui_MainUI')
            shutil.copy(file[0], os.path.join(basemoddic, os.path.basename(file[0])))
            self.refresh_data()

    def addFile_zip(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setWindowIcon(QIcon(ICONPATH))
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Zip file', filter="Zip file (*.zip)")
        if file[0]:
            with zipfile.ZipFile(file[0], 'r', metadata_encoding='gbk') as zip_ref:
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

            self.refresh_data()

    def handleCheckboxStateChange(self, state, index):
        if state == 2:
            enablemod(index)
        elif state == 0:
            disablemod(index)

    def setprogressbarvalue(self, progress:int):
        self.ui.progressBar.setValue(progress)

    def auto_refresh(self):
        lj.info('refresh thread start')
        global last_refresh
        last_refresh = datetime.datetime.now().timestamp()
        while not stop_event.is_set():
            if datetime.datetime.now().timestamp() - last_refresh >= 60:
                lj.info('auto refreshing...')
                self.refresh_signal.emit()
                last_refresh = datetime.datetime.now().timestamp()
            stop_event.wait(1)  # Check the event every second
        lj.info('refresh thread stop')

    def closeEvent(self):
        global stop_event
        # Set the stop event to signal the refresh thread to stop
        stop_event.set()
        # Wait for the refresh thread to finish
        refresh.join()
        lj.info(refresh.is_alive())
        
        self.close()
class OperationUi(QtWidgets.QDialog):
    def __init__(self, index):
        super().__init__()
        lj.info('showing OperationUi with index %s' % index+', pos='+'Ui_OperationUi')
        self.ui = Dialog_mod_operation()
        self.ui.setupUi(self)
        self.ui.pushButton_del.clicked.connect(
            lambda checked: self.handle_del(index)
        )
        self.ui.pushButton_endisable.clicked.connect(
            lambda checked: self.handle_stat_change(index)
        )
        self.setWindowIcon(QIcon(ICONPATH))

        self.show()

    def handle_del(self, index):
        self.close()
        Op_ConfirmUi(index, in_lang['Operation.Confirmdel'], {'confirm': f'delmod({index})'})

    def handle_stat_change(self, index):
        self.close()
        if mod_database['mod' + str(index)]['active'] == 'True':
            disablemod(index)
        else:
            enablemod(index)

class ConfirmUi(QtWidgets.QDialog):
    def __init__(self, index, text, operation):
        super().__init__()
        lj.info('showing ConfirmUi with keys: (%s,%s,%s)' % (index, text, operation)+', pos='+'Ui_ConfirmUi')
        self.operation = operation
        self.index = index
        self.ui = Dialog_check_yn()
        self.ui.setupUi(self)
        self.ui.textBrowser.setText(text)
        self.setWindowIcon(QIcon(ICONPATH))
        self.show()

    def accept(self):
        self.done(1)
        if 'confirm' in self.operation:
            exec(self.operation['confirm'])

    def reject(self):
        self.done(0)
        if 'reject' in self.operation:
            exec(self.operation['reject'])

def Op_OperationUi(index):
    Operationwindow = OperationUi(index)
    Operationwindow.exec()

def Op_ConfirmUi(index, text, operation):
    Confirmwindow = ConfirmUi(index, text, operation)
    Confirmwindow.exec()

def load_translator():
    global translator, in_lang
    lj.info(f'trans:{QLocale.system().language()}')
    lang = QLocale.system().language()
    # Load the appropriate .qm file based on the locale
    if lang == QLocale.Language.Chinese:
        translator.load(r'.\Ui\Main_zh_CN.qm')
        in_lang = {
            'Operation.Confirmdel': '确认删除?文件将被移动到回收站',
            'Operation.operation': '操作',
            'label.0': 'Mod',
            'label.1': '版本',
            'label.2': '状态',
            'label.3': '操作',
            'warning.dumplicate_mod_higher_ver': '更高或相同版本的同Mod处在启用状态！'
        }
    # elif QLocale.Language() == QLocale.Language.AnyLanguage:
    #     translator.load(r'.\Ui\Main_zh_CN.qm')
    elif lang == QLocale.Language.English:
        in_lang = {
            'Operation.Confirmdel': 'Confirm deletion? The file will be moved to the recycle bin',
            'Operation.operation': 'Operation',
            'label.0': 'Mod',
            'label.1': 'Version',
            'label.2': 'Status',
            'label.3': 'Operation',
            'warning.dumplicate_mod_higher_ver': '''The same mod with a higher or same version is in active mode!
Aborting'''
        }
    else:
        # Default to English if the locale is not supported
        in_lang = {
            'Operation.Confirmdel': 'Confirm deletion? The file will be moved to the recycle bin',
            'Operation.operation': 'Operation',
            'label.0': 'Mod',
            'label.1': 'Version',
            'label.2': 'Status',
            'label.3': 'Operation',
            'warning.dumplicate_mod_higher_ver': '''The same mod with a higher or same version is in active mode!
Aborting'''
        }


if __name__ == '__main__':

    try:
        app = QApplication(sys.argv)
        translator = QTranslator(app)
        load_translator()
        app.installTranslator(translator)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
        Mainwindow = ModMannager_MainUI()
        app.exec()
        sys.exit(stop_event.set())
    except Exception as E:
        stop_event.set()
        lj.warning(f'error occurred:\n{traceback.format_exc()}')
        lj.info(f'db:\n{mod_database}')
        lj.info('ver: %s os: %s' % (ver, platform.system())+',pos='+'exechandler')
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(ICONPATH))
        msg_box.setText("""please upload the latest log after the whole program is exited\n(after the window is closed).
the log file is in 'MiniAirways_mod_manager_log' folder.""")
        msg_box.exec()
        sys.exit()


# add: search dumplicate->
'''
enable:
search dumplicate -> higher -> enable/disable(old)
                  -> lower  -> abort
disable:
disable
add:
search dumplicate -> higher -> enable/disable(old)
                  -> lower  -> add&disable
'''





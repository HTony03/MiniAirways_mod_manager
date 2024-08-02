import os
import sys
# from PySide6 import *
import platform
import time
import json

import loggerjava as lj

if not os.path.exists('.\\MiniAirways_mod_manager_log\\'):
    os.mkdir('.\\MiniAirways_mod_manager_log\\')
if not os.path.exists('.\\BepInEx\\'):
    print('the mod manager is currently not in the Mini Airways Folder')
    print('check your location and open the manager!')
    os.system('pause')
    exit(0)

lj.config(name='.\\MiniAirways_mod_manager_log\\' +
               str(time.gmtime().tm_mon) + '.' + str(time.gmtime().tm_mday) + '_' +
               str(time.gmtime().tm_hour) + '.' + str(time.gmtime().tm_min)
          , showinconsole=False)
lj.clearcurrentlog()
lj.debug('current loggerjava ver:' + lj.ver, pos='test_loggerjava')

mod_database = {}
basemoddic = r'.\BepInEx\plugins\\'
ver = '0.1.1'
commander = ['[bs] ', '>>> ']
command_sel = 1
sys.path.extend(r'.//ReferencedAssemblies')
last_refresh = time.time()
import clr

try:
    def reload_from_disc():
        global mod_database, last_refresh
        mod_database = {}
        name_db_in = []
        stat_db_in = []
        # TODO!!!: FileExistsError(same name)
        for filename in os.listdir(basemoddic):
            if os.path.isfile(os.path.join(basemoddic, filename)):
                base, ext = os.path.splitext(filename)
                while ext and base.count('.') > 0:
                    base, new_ext = os.path.splitext(base)
                    ext = new_ext + ext

                if ext == '.dll':
                    module = clr.AddReference(basemoddic + base)
                    modulename = module.ToString().split(', ')[0]
                    if ((modulename not in name_db_in) or
                            (modulename in name_db_in and not stat_db_in[name_db_in.index(modulename)])):
                        mod_database['mod' + str(len(mod_database))] = {
                            "name": module.ToString().split(', ')[0],
                            "file_name": base + '.dll',
                            'ver': module.ToString().split(', ')[1].split('=')[1],
                            "active": "True"
                        }
                        name_db_in.append(module.ToString().split(', ')[0])
                        stat_db_in.append(1)
                    else:
                        # 3个重复以上修改为查询所有然后处理
                        # test ver
                        original_ver = mod_database['mod' + str(name_db_in.index(modulename))]['ver']
                        now_ver = module.ToString().split(', ')[1].split('=')[1]
                        if now_ver > original_ver:
                            lj.warn(
                                'read file:%s is the same mod of different version, auto disabling the lower version '
                                'one'
                                % filename)
                            os.rename(mod_database['mod' + str(name_db_in.index(modulename))]['file_name'],
                                      mod_database['mod' + str(name_db_in.index(modulename))][
                                          'file_name'] + '.disabled')
                            mod_database['mod' + str(name_db_in.index(modulename))]['active'] = 'False'
                            stat_db_in[name_db_in.index(module.ToString().split(', ')[0])] = 0

                            mod_database['mod' + str(len(mod_database))] = {
                                "name": module.ToString().split(', ')[0],
                                "file_name": base + '.dll',
                                'ver': module.ToString().split(', ')[1].split('=')[1],
                                "active": "True"
                            }

                            name_db_in.append(module.ToString().split(', ')[0])
                            stat_db_in.append(1)

                        elif now_ver < original_ver:
                            lj.warn(
                                'read file:%s is the same mod of different version, auto disabling the lower version '
                                'one'
                                % filename)
                            os.rename(os.path.join(basemoddic, filename),
                                      os.path.join(basemoddic, filename + '.disabled'))
                            mod_database['mod' + str(len(mod_database))] = {
                                "name": module.ToString().split(', ')[0],
                                "file_name": base + '.dll',
                                'ver': module.ToString().split(', ')[1].split('=')[1],
                                "active": "False"
                            }

                            name_db_in.append(module.ToString().split(', ')[0])
                            stat_db_in.append(0)
                        else:
                            lj.warn('read file:%s is the same mod of the same version, auto disabling the current one'
                                    % filename)
                            os.rename(os.path.join(basemoddic, filename),
                                      os.path.join(basemoddic, filename + '.disabled'))
                            mod_database['mod' + str(len(mod_database))] = {
                                "name": module.ToString().split(', ')[0],
                                "file_name": base + '.dll',
                                'ver': module.ToString().split(', ')[1].split('=')[1],
                                "active": "False"
                            }
                            name_db_in.append(module.ToString().split(', ')[0])
                            stat_db_in.append(0)
                if ext == '.dll.disabled':
                    os.rename(os.path.join(basemoddic, filename), os.path.join(basemoddic, base + '.dll'))
                    module = clr.AddReference(basemoddic + base)
                    mod_database['mod' + str(len(mod_database))] = {
                        "name": module.ToString().split(', ')[0],
                        "file_name": base + '.dll',
                        'ver': module.ToString().split(', ')[1].split('=')[1],
                        "active": "False"
                    }
                    name_db_in.append(module.ToString().split(', ')[0])
                    stat_db_in.append(0)
                    os.rename(os.path.join(basemoddic, base + '.dll'), os.path.join(basemoddic, filename))
        last_refresh = time.time()
        lj.info("loaded mods from disc!")


    def delmod(index):
        global mod_database

        print('mod to be deleted:' + mod_database['mod' + str(index)]['name'])
        confirm = input('input "Confirm" to confirm the deletion of the mod:')
        if confirm != "Confirm":
            print("confirmation aborted!")
            return
        filedir = mod_database['mod' + str(index)]['file_name']
        dll_file_path = r'.\BepInEx\plugins\\' + filedir
        if os.path.exists(dll_file_path):
            os.remove(dll_file_path)
            print(f"Mod file file {dll_file_path} has been deleted.")
        elif os.path.exists(dll_file_path + ".disabled"):
            os.remove(dll_file_path + ".disabled")
            print(f"Mod file file {dll_file_path}.disabled has been deleted.")
        else:
            print(f"Mod file {dll_file_path} does not exist.\n"
                  f"removing the related mod data")

        print("deleted!")


    def enablemod(index):
        # TODO:check whether have dumplicate mods enabled(先两个后多个compact)
        global mod_database
        filedir = mod_database['mod' + str(index)]['file_name']

        if mod_database['mod' + str(index)]['active'] != "False":
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\n aborting and refreshing... ")
            reload_from_disc()
            return
        if not os.path.exists(basemoddic + filedir + '.disabled'):
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\n aborting and refreshing... ")
            mod_database['mod' + str(index)]['active'] = "False"
            reload_from_disc()
            return
        os.rename(basemoddic + filedir + '.disabled', basemoddic + filedir)
        mod_database['mod' + str(index)]['active'] = "True"
        print("changed mod " + mod_database['mod' + str(index)]['name'] + ' status to enabled')


    def disablemod(index):
        global mod_database
        filedir = mod_database['mod' + str(index)]['file_name']

        if mod_database['mod' + str(index)]['active'] != "True":
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\naborting and refreshing... ")
            reload_from_disc()
            return
        if not os.path.exists(basemoddic + filedir):
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\naborting and refreshing... ")
            mod_database['mod' + str(index)]['active'] = "False"
            reload_from_disc()
            return
        os.rename(basemoddic + filedir, basemoddic + filedir + '.disabled')
        mod_database['mod' + str(index)]['active'] = "False"
        print("changed mod " + mod_database['mod' + str(index)]['name'] + ' status to disabled')


    lj.register_def(reload_from_disc)
    lj.register_def(delmod)
    lj.register_def(enablemod)
    lj.register_def(disablemod)
    reload_from_disc()

    if __name__ == '__main__':
        reload_from_disc()
        lj.info('read mods:' + json.dumps(mod_database, ensure_ascii=True, indent=4, sort_keys=False))
        pass
    print('Mini Airways Mod manager %s on %s' % (ver, platform.system()))
    print('Type "help" for command usages')

    # TODO:change the index to 1,2,3,.... rather than 0,1,2,.....

    while True:
        commandd = input(commander[command_sel])
        # TODO:UI & 30s auto refresh
        commandlist = commandd.split(' ')
        command = commandlist[0]
        lj.info('user choice:' + command)
        if command == 'disablemod':
            p = False
            if len(commandlist) > 1:
                try:
                    indexx = int(commandlist[1])
                    if 0 <= indexx < len(mod_database):
                        p = True
                        pass
                except ValueError:
                    print("invaid index")
            while True:
                if p:
                    break
                try:
                    indexx = int(input("mod index:"))
                    if 0 <= indexx < len(mod_database):
                        break
                    print("invaid index")
                except ValueError:
                    print("invaid index")
            if mod_database['mod' + str(indexx)]['active'] == "False":
                print("the mod is currently not active!")
                print("if the status is not the same as it in the disc, please use \"refresh_mod_file_stat\".")
            else:
                disablemod(indexx)
        elif command == 'enablemod':
            p = False
            if len(commandlist) > 1:
                try:
                    indexx = int(commandlist[1])
                    if 0 <= indexx < len(mod_database):
                        p = True
                        pass
                except ValueError:
                    print("invaid index")
            while True:
                if p:
                    break
                try:
                    indexx = int(input("mod index:"))
                    if 0 <= indexx < len(mod_database):
                        break
                    print("invaid index")
                except ValueError:
                    print("invaid index")
            if mod_database['mod' + str(indexx)]['active'] == "True":
                print("the mod is currently active!")
                print("if the status is not the same as it in the disc, please use \"refresh_mod_file_stat\".")
            else:
                enablemod(indexx)
        elif command == 'delmod':
            p = False
            if len(commandlist) > 1:
                try:
                    indexx = int(commandlist[1])
                    if 0 <= indexx < len(mod_database):
                        p = True
                        pass
                except ValueError:
                    print("invaid index")
            while True:
                if p:
                    break
                try:
                    indexx = int(input("mod index:"))
                    if 0 <= indexx < len(mod_database):
                        break
                    print("invaid index")
                except ValueError:
                    print("invaid index")
            delmod(indexx)

        elif command == "showmods":
            reload_from_disc()
            for i in range(len(mod_database)):
                print('mod name:%s' % mod_database['mod' + str(i)]['name'])
                if 'ver' in mod_database['mod' + str(i)]:
                    print('mod version:%s' % mod_database['mod' + str(i)]['ver'])
                print('mod index:%s' % i)
                print('mod file:%s' % mod_database['mod' + str(i)]['file_name'])
                if mod_database['mod' + str(i)]['active'] == "True":
                    print('mod status:Enabled')
                else:
                    print('mod status:Disabled')
                print("")
        elif command == 'reload':
            reload_from_disc()
        elif command == 'rungame':
            os.system(r'.\MiniAirways.exe')
        elif command == 'exit':
            break
        elif command == 'help':
            print("""
disablemod:
disable a mod

enablemod:
enable a mod

delmod:
delete a mod

showmods:
show the mods that are loaded in the database

reload:
mannually refresh mods from disc

rungame:
run the game!

help:
show all the usages of the commands

exit:
exit the program""")

    lj.info('closing')
    os.system("pause")
except Exception as E:
    lj.warn(lj.handler(E), pos='exechandler', showinconsole=True)
    lj.info('db:\n' + json.dumps(mod_database, ensure_ascii=True, indent=4, sort_keys=False), pos='exechandler')
    lj.info('ver: %s os: %s' % (ver, platform.system()), pos='exechandler')
    print('please upload the latest log after the whole program is exited(after the console is closed).')
    print("the log is in 'MiniAirways_mod_manager_log' folder.")
    os.system('pause')

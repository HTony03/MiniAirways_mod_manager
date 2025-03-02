import json
import os
# from PySide6 import *
import platform
import sys
import threading
import time

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
               str(time.gmtime().tm_hour) + '.' + str(time.gmtime().tm_min), showinconsole=False)
lj.clearcurrentlog()
lj.debug('current loggerjava ver:' + lj.ver, pos='test_loggerjava')

mod_database = {}
basemoddic = r'.\BepInEx\plugins\\'
ver = '0.2.1'
commander = ['[bs] ', '>>> ']
command_sel = 1
sys.path.extend(r'.//ReferencedAssemblies')
last_refresh = time.time()
import clr

try:
    def reload_from_disc():
        global mod_database, last_refresh
        mod_database = {}
        name_db = []
        stat_db = []
        for filename in os.listdir(basemoddic):
            if os.path.isfile(os.path.join(basemoddic, filename)):
                base, ext = os.path.splitext(filename)
                while ext and base.count('.') > 0:
                    base, new_ext = os.path.splitext(base)
                    ext = new_ext + ext

                if ext == '.dll':
                    module = clr.AddReference(basemoddic + base)
                    modulename = module.ToString().split(', ')[0]
                    if ((modulename not in name_db) or
                            (modulename in name_db and not stat_db[name_db.index(modulename)])):
                        mod_database['mod' + str(len(mod_database))] = {
                            "name": module.ToString().split(', ')[0],
                            "file_name": base + '.dll',
                            'ver': module.ToString().split(', ')[1].split('=')[1],
                            "active": "True"
                        }
                        name_db.append(module.ToString().split(', ')[0])
                        stat_db.append(1)
                    else:
                        # 3个重复以上修改为查询所有然后处理
                        # test ver
                        original_ver = mod_database['mod' + str(name_db.index(modulename))]['ver']
                        now_ver = module.ToString().split(', ')[1].split('=')[1]
                        if now_ver > original_ver:
                            lj.warn(
                                'read file:%s is the same mod of different version, auto disabling the lower version '
                                'one'
                                % filename, pos='refresh_mod_thread')
                            os.rename(mod_database['mod' + str(name_db.index(modulename))]['file_name'],
                                      mod_database['mod' + str(name_db.index(modulename))][
                                          'file_name'] + '.disabled')
                            mod_database['mod' + str(name_db.index(modulename))]['active'] = 'False'
                            stat_db[name_db.index(module.ToString().split(', ')[0])] = 0

                            mod_database['mod' + str(len(mod_database))] = {
                                "name": module.ToString().split(', ')[0],
                                "file_name": base + '.dll',
                                'ver': module.ToString().split(', ')[1].split('=')[1],
                                "active": "True"
                            }

                            name_db.append(module.ToString().split(', ')[0])
                            stat_db.append(1)

                        elif now_ver < original_ver:
                            lj.warn(
                                'read file:%s is the same mod of different version, auto disabling the lower version '
                                'one'
                                % filename, pos='refresh_mod_thread')
                            os.rename(os.path.join(basemoddic, filename),
                                      os.path.join(basemoddic, filename + '.disabled'))
                            mod_database['mod' + str(len(mod_database))] = {
                                "name": module.ToString().split(', ')[0],
                                "file_name": base + '.dll',
                                'ver': module.ToString().split(', ')[1].split('=')[1],
                                "active": "False"
                            }

                            name_db.append(module.ToString().split(', ')[0])
                            stat_db.append(0)
                        else:
                            lj.warn('read file:%s is the same mod of the same version, auto disabling the current one'
                                    % filename, pos='refresh_mod_thread')
                            os.rename(os.path.join(basemoddic, filename),
                                      os.path.join(basemoddic, filename + '.disabled'))
                            mod_database['mod' + str(len(mod_database))] = {
                                "name": module.ToString().split(', ')[0],
                                "file_name": base + '.dll',
                                'ver': module.ToString().split(', ')[1].split('=')[1],
                                "active": "False"
                            }
                            name_db.append(module.ToString().split(', ')[0])
                            stat_db.append(0)
                if ext == '.dll.disabled':
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
                        print('hmmmm what do you want do to XD\nskipping the file')
                        continue
                    module = clr.AddReference(basemoddic + base)
                    mod_database['mod' + str(len(mod_database))] = {
                        "name": module.ToString().split(', ')[0],
                        "file_name": base + '.dll',
                        'ver': module.ToString().split(', ')[1].split('=')[1],
                        "active": "False"
                    }
                    # print(base)
                    # print(filename)
                    name_db.append(module.ToString().split(', ')[0])
                    stat_db.append(0)
                    os.rename(changed_name, os.path.join(basemoddic, filename))
        last_refresh = time.time()
        lj.info("loaded mods from disc!", pos='refresh_mod_thread')

    def refresh_thread():
        while 1:
            reload_from_disc()
            time.sleep(60)


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
            print(f"Mod file file %s has been deleted." % dll_file_path)
        elif os.path.exists(dll_file_path + ".disabled"):
            os.remove(dll_file_path + ".disabled")
            print(f"Mod file file %s.disabled has been deleted." % dll_file_path)
        else:
            print(f"Mod file %s does not exist.\n" % dll_file_path +
                  f"removing the related mod data")
        lj.info('deleting mod with index %s' % index)
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
        lj.info('disabling mod with index %s' % index)
        print("changed mod " + mod_database['mod' + str(index)]['name'] + ' status to disabled')

    def Main():
        lj.info('read mods:' + json.dumps(mod_database, ensure_ascii=True, indent=4, sort_keys=False))
        while True:
            commandd = input(commander[command_sel])
            # TODO:UI
            commandlist = commandd.split(' ')
            command = commandlist[0]
            lj.info('user choice:' + str(commandlist))
            if command == 'disablemod':
                p = False
                if len(commandlist) > 1:
                    try:
                        indexx = int(commandlist[1])
                        if 1 <= indexx < len(mod_database) + 1:
                            p = True
                    except ValueError:
                        print("invaid index")
                while True:
                    if p:
                        break
                    try:
                        indexx = int(input("mod index:"))
                        if 1 <= indexx < len(mod_database) + 1:
                            break
                        print("invaid index")
                    except ValueError:
                        print("invaid index")
                indexx -= 1
                if mod_database['mod' + str(indexx)]['active'] == "False":
                    print("the mod is currently not active!")
                    print("if the status is not the same as it in the disc, please use \"reload\".")
                else:
                    disablemod(indexx)
            elif command == 'enablemod':
                p = False
                if len(commandlist) > 1:
                    try:
                        indexx = int(commandlist[1])
                        if 1 <= indexx < len(mod_database) + 1:
                            p = True
                    except ValueError:
                        print("invaid index")
                while True:
                    if p:
                        break
                    try:
                        indexx = int(input("mod index:"))
                        if 1 <= indexx < len(mod_database) + 1:
                            break
                        print("invaid index")
                    except ValueError:
                        print("invaid index")
                indexx -= 1
                if mod_database['mod' + str(indexx)]['active'] == "True":
                    print("the mod is currently active!")
                    print("if the status is not the same as it in the disc, please use \"reload\".")
                else:
                    enablemod(indexx)
            elif command == 'delmod':
                p = False
                if len(commandlist) > 1:
                    try:
                        indexx = int(commandlist[1])
                        if 1 <= indexx < len(mod_database) + 1:
                            p = True
                    except ValueError:
                        print("invaid index")
                while True:
                    if p:
                        break
                    try:
                        indexx = int(input("mod index:"))
                        if 1 <= indexx < len(mod_database) + 1:
                            break
                        print("invaid index")
                    except ValueError:
                        print("invaid index")
                delmod(indexx - 1)

            elif command == "showmods":
                reload_from_disc()
                for i in range(len(mod_database)):
                    print('mod name:%s' % mod_database['mod' + str(i)]['name'])
                    if 'ver' in mod_database['mod' + str(i)]:
                        print('mod version:%s' % mod_database['mod' + str(i)]['ver'])
                    print('mod index:%s' % (i + 1))
                    print('mod file:%s' % mod_database['mod' + str(i)]['file_name'])
                    if mod_database['mod' + str(i)]['active'] == "True":
                        print('mod status:Enabled')
                    else:
                        print('mod status:Disabled')
                    print("")
            elif command == 'addmod':
                if len(commandlist) > 1:
                    route = ' '.join(commandlist[1:])
                else:
                    route = input("mod route:")
                print(route)
                if not os.path.exists(route):
                    print('the mod route is invalid, aborthing')
                else:
                    os.system('copy "%s" %s' % (route, basemoddic+os.path.basename(route)))
            elif command == 'reload':
                reload_from_disc()
            elif command == 'rungame':
                os.system(r'.\MiniAirways.exe')
            elif command == 'exit':
                break
            elif command == 'openfolder':
                os.system('explorer ' + os.path.abspath(basemoddic))
            elif command == 'help':
                print("""
addmod:
add a mod with the dll location (full path)

delmod:
delete a mod

disablemod:
disable a mod

enablemod:
enable a mod

showmods:
show the mods that are loaded in the database

reload:
mannually refresh mods from disc
will automantically disable the dumplicate mods and keep the higher version

rungame:
run the game!

openfolder:
open the mod folder

help:
show all the usages of the commands

exit:
exit the program""")

        lj.info('closing')
        os.system("pause")


    lj.register_def(reload_from_disc)
    lj.register_def(delmod)
    lj.register_def(enablemod)
    lj.register_def(disablemod)
    lj.register_def(refresh_thread)
    lj.register_def(Main)
    refreshing_thread = threading.Thread(target=refresh_thread)
    Main_thread = threading.Thread(target=Main)

    refreshing_thread.start()

    if __name__ == '__main__':
        pass
    print('Mini Airways Mod manager %s on %s' % (ver, platform.system()))
    print('Type "help" for command usages')
    Main_thread.start()

except Exception as E:
    lj.warn(lj.handler(E), pos='exechandler', showinconsole=True)
    lj.info('db:\n' + json.dumps(mod_database, ensure_ascii=True, indent=4, sort_keys=False), pos='exechandler')
    lj.info('ver: %s os: %s' % (ver, platform.system()), pos='exechandler')
    print('please upload the latest log after the whole program is exited(after the console is closed).')
    print("the log is in 'MiniAirways_mod_manager_log' folder.")
    os.system('pause')

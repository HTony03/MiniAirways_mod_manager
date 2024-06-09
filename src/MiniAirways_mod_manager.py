import json
import os
import zipfile
import platform

import loggerjava as lj
from json import JSONDecodeError

if __name__ == "__main__":
    pass

lj.config(name='MiniAirways_mod_manager_log', showinconsole=False)
lj.clearcurrentlog()
lj.debug('current loggerjava ver:' + lj.ver)
mod_database_loc = r'.\MiniAirways_mod_manager_database.json'
mod_database = {}
basemoddic = r'.\BepInEx\plugins\\'
ver = '0.0.1.dev'

try:

    def loaddatabase():
        global mod_database
        try:
            if os.path.exists(mod_database_loc):
                with open(mod_database_loc, 'r') as f:
                    mod_database = json.load(f)
                    lj.debug('read database:\n' + str(mod_database))
            else:
                with open(mod_database_loc, 'x+'):
                    pass
                print('database not exist, creating a new one')
                mod_database = {}
                lj.debug('no database read')
        except JSONDecodeError:
            print("error while decoding the database")
            print("please del the database and reopen the program!")
            os.system("pause")
            exit(10)


    def refresh_exist_mods():
        global mod_database
        file_db = []
        for i in range(len(mod_database)):
            file_db.append(mod_database['mod' + str(i)]["file_name"])

        for filename in os.listdir(basemoddic):
            if os.path.isfile(os.path.join(basemoddic, filename)):

                base, ext = os.path.splitext(filename)
                # 如果base中还有'.'，则继续分割
                while ext and base.count('.') > 0:
                    base, new_ext = os.path.splitext(base)
                    ext = new_ext + ext

                if filename not in file_db:
                    if ext != ".dll.disable":
                        mod_database['mod' + str(len(mod_database))] = {
                            "name": base,
                            "desc": "none",
                            "file_name": base + '.dll',
                            "dependencies": 0,
                            "active": "True"
                        }
                    else:
                        mod_database['mod' + str(len(mod_database))] = {
                            "name": base,
                            "desc": "none",
                            "file_name": base + '.dll',
                            "dependencies": 0,
                            "active": "False"
                        }
                else:
                    # mod_index = file_db.index(base + '.dll')

                    file_db = []
                    for i in range(len(mod_database)):
                        file_db.append(mod_database['mod' + str(i)]["file_name"])

                    if ext != ".dll.disable":
                        mod_database['mod' + str(file_db.index(base + '.dll'))]['active'] = "True"
                    else:
                        mod_database['mod' + str(file_db.index(base + '.dll'))]['active'] = "False"

        print("loaded mods from disc!")


    def refresh_mod_status():
        global mod_database
        resort_db()
        for i in range(len(mod_database)):
            listmod = mod_database['mod' + str(i)]
            if os.path.exists(basemoddic + listmod["file_name"]):
                mod_database['mod' + str(i)]["active"] = "True"
            elif os.path.exists(basemoddic + listmod['file_name'] + '.disabled'):
                mod_database['mod' + str(i)]['active'] = 'False'
            else:
                print("mod does not exist, deleting related data.")
                mod_database.pop('mod' + str(i))
        resort_db()
        print('refreshed database!')


    def addmod(fileroute):
        global mod_database
        resort_db()
        with zipfile.ZipFile(fileroute) as zipfile_obj:
            with zipfile_obj.open('meta-inf.json') as f:
                content = f.read()

                if isinstance(content, bytes):
                    content = content.decode('utf-8')

                data = json.loads(content)
        print('read mod name:%s' % data['name'])
        print('read mod description:%s' % data['desc'])
        choice = input('Continue adding procedure?(Y/N):')
        if choice != 'Y':
            print('add aborted!')
            return
        file_db = []
        for i in range(len(mod_database)):
            file_db.append(mod_database['mod' + str(i)]["file_name"])
        if data['file_name'] in file_db:
            print("mod exist!")
            return
        if data['dependencies']:
            for i in data['dependencies']:
                if i == 0:
                    pass
                if i['file'] in file_db:
                    status = mod_database['mod' + str(file_db.index(i['file']))]['status']
                    if status != "True":
                        print("the dependence mod:%s is not activated, auto active the mod")
                        enablemod(file_db.index(i['file']))
                else:
                    print("the dependence mod:%s does not exist.\nplease install it before installing %s!"
                          % (i['name'], data['name']))
                    return
        data['active'] = "True"
        with zipfile.ZipFile(fileroute, 'r') as zip_ref:
            extracted = False
            for file_info in zip_ref.infolist():
                if file_info.filename == data['file_name']:
                    zip_ref.extract(file_info, r'.\BepInEx\plugins\\')
                    extracted = True
            if not extracted:
                print('did not find the mod file related to the meta-inf.json')
                print('consider the zip/meta-inf.json is broken')
            else:
                mod_database['mod' + str(len(mod_database))] = data
                print("successfully added the mod:%s!" % data['name'])


    def delmod(index):
        global mod_database

        file_db = []
        status_db = []
        for i in range(len(mod_database)):
            file_db.append(mod_database['mod' + str(i)]["dependencies"])
            status_db.append(mod_database['mod' + str(i)]["active"])

        dependened = []
        for i in file_db:
            if i == 0:
                continue
            for j in i:
                if j['name'] == mod_database['mod' + str(index)]['name'] and status_db[file_db.index(i)] == 'True':
                    dependened.append(mod_database['mod' + str(file_db.index(i))]['name'])
        if dependened:
            print('the mod %s is dependented by mod %s!\nplease diable them before removing!' % (
                mod_database['mod' + str(index)]['name'], dependened))
            return

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
        mod_database.pop('mod' + str(index))
        resort_db()
        print("deleted!")


    def enablemod(index):
        global mod_database
        filedir = mod_database['mod' + str(index)]['file_name']

        name_db = []
        status_db = []
        for i in range(len(mod_database)):
            name_db.append(mod_database['mod' + str(i)]["name"])
            status_db.append(mod_database['mod' + str(i)]["active"])
        passtest = True
        if mod_database['mod' + str(index)]['dependencies']:
            for i in mod_database['mod' + str(index)]['dependencies']:
                if i['name'] in name_db:
                    if status_db[name_db.index(i['name'])] != "True":
                        print("the dependence mod:%s is not activated." % i['name'])
                        passtest = False
                else:
                    print("the dependence mod:%s does not in the database." % i['name'])
                    print("if you've installed but still have this tip please reload "
                          "the mods from disc using \"loadfromdisc\"")
                    passtest = False
        if not passtest:
            print("dependence test failed.")
            return

        if mod_database['mod' + str(index)]['active'] != "False":
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\n aborting and refreshing... ")
            refresh_exist_mods()
            return
        if not os.path.exists(basemoddic + filedir + '.disabled'):
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\n aborting and refreshing... ")
            mod_database['mod' + str(index)]['active'] = "False"
            refresh_exist_mods()
            return
        os.rename(basemoddic + filedir + '.disabled', basemoddic + filedir)
        mod_database['mod' + str(index)]['active'] = "True"
        print("changed mod " + mod_database['mod' + str(index)]['name'] + ' status to enabled')


    def disablemod(index):
        global mod_database
        filedir = mod_database['mod' + str(index)]['file_name']
        #
        file_db = []
        status_db = []
        for i in range(len(mod_database)):
            file_db.append(mod_database['mod' + str(i)]["dependencies"])
            status_db.append(mod_database['mod' + str(i)]["active"])

        dependened = []
        for i in file_db:
            if i == 0:
                continue
            for j in i:
                if j['name'] == mod_database['mod' + str(index)]['name'] and status_db[file_db.index(i)] == 'True':
                    dependened.append(mod_database['mod' + str(file_db.index(i))]['name'])
        if dependened:
            print('the mod %s is dependented by mod %s!\nplease diable them before disabling!' % (
                mod_database['mod' + str(index)]['name'], dependened))
            return
        #
        if mod_database['mod' + str(index)]['active'] != "True":
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\naborting and refreshing... ")
            refresh_exist_mods()
            return
        if not os.path.exists(basemoddic + filedir):
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\naborting and refreshing... ")
            mod_database['mod' + str(index)]['active'] = "False"
            refresh_exist_mods()
            return
        os.rename(basemoddic + filedir, basemoddic + filedir + '.disabled')
        mod_database['mod' + str(index)]['active'] = "False"
        print("changed mod " + mod_database['mod' + str(index)]['name'] + ' status to disabled')


    def showdesc(index):
        return mod_database['mod' + str(index)]['desc']


    def resort_db():
        global mod_database
        new_db = {}
        for index, data in mod_database.items():
            new_db['mod' + str(len(new_db))] = data
        mod_database = new_db


    # Main

    lj.register_def(loaddatabase)
    lj.register_def(refresh_exist_mods)
    lj.register_def(refresh_mod_status)
    lj.register_def(addmod)
    lj.register_def(delmod)
    lj.register_def(enablemod)
    lj.register_def(disablemod)
    lj.register_def(showdesc)
    lj.register_def(resort_db)

    loaddatabase()
    refresh_mod_status()
    refresh_exist_mods()
    resort_db()

    print('Mini Airways Mod manager %s on %s' % (ver, platform.system()))
    print('Type "help" for command usages')

    # TODO: diff ver compact
    # TODO: new command format

    while True:
        command = input('[bs] ')
        lj.debug('user choice:' + command)
        if command == 'addmod':
            route = input('input the path of your downloaded mod zip file location:')
            addmod(route)
        elif command == 'disablemod':
            while True:
                try:
                    indexx = int(input("mod index:"))
                    if 0 <= indexx < len(mod_database):
                        break
                except ValueError:
                    print("invaid index")
            if mod_database['mod' + str(indexx)]['active'] == "False":
                print("the mod is currently not active!")
                print("if the status is not the same as it in the disc, please use \"refresh_mod_file_stat\".")
            else:
                disablemod(indexx)
        elif command == 'enablemod':
            while True:
                try:
                    indexx = int(input("mod index:"))
                    if 0 <= indexx < len(mod_database):
                        break
                except ValueError:
                    print("invaid index")
            if mod_database['mod' + str(indexx)]['active'] == "True":
                print("the mod is currently active!")
                print("if the status is not the same as it in the disc, please use \"refresh_mod_file_stat\".")
            else:
                enablemod(indexx)
        elif command == 'delmod':
            while True:
                try:
                    indexx = int(input("mod index:"))
                    if 0 <= indexx < len(mod_database):
                        break
                except ValueError:
                    print("invaid index")
            delmod(indexx)

        elif command == "showmods":
            resort_db()
            for i in range(len(mod_database)):
                print('mod name:%s' % mod_database['mod' + str(i)]['name'])
                if 'ver' in mod_database['mod' + str(i)]:
                    print('mod version:%s' % mod_database['mod' + str(i)]['ver'])
                print('mod index:%s' % i)
                print('mod description:%s' % mod_database['mod' + str(i)]['desc'])
                print('mod dependences:')
                if mod_database['mod' + str(i)]["dependencies"]:
                    for k in mod_database['mod' + str(i)]["dependencies"]:
                        print('dependence %s name:%s' % (
                            mod_database['mod' + str(i)]['dependencies'].index(k) + 1, k['name']))
                else:
                    print("None")
                if mod_database['mod' + str(i)]['active'] == "True":
                    print('mod status:Enabled')
                else:
                    print('mod status:Disabled')
                print("")
        elif command == 'refresh_db':
            resort_db()
        elif command == 'refresh_mod_file_stat':
            refresh_mod_status()
        elif command == 'loadfromdisc':
            refresh_exist_mods()
        elif command == 'rungame':
            os.system(r'.\MiniAirways.exe')
        elif command == 'exit':
            break
        elif command == 'help':
            print("""
addmod:
add a new mod

disablemod:
disable a mod

enablemod:
enable a mod

delmod:
delete a mod

showmods:
show the mods that are loaded in the database

refresh_db:
mannually refresh the database

refresh_mod_file_stat:
refresh the mod status from disc
will automantically delete the nonexist mod data

loadfromdisc:
load mods from disc
will automantically add mods that are not in database

help:
show all the usages of the commands

exit:
exit the program and save the database
            """)
    print("saving database")
    lj.debug('saving db:' + str(mod_database))
    with open(mod_database_loc, mode='w') as f:
        json.dump(mod_database, f, ensure_ascii=False, indent=4)
    lj.debug('closing')
    os.system("pause")
except Exception as E:
    lj.config(showinconsole=True)
    lj.warn(lj.handler(E))
    lj.debug('db:\n' + str(mod_database))
    lj.debug('ver: %s os: %s' % (ver, platform.system()))
    os.system('pause')

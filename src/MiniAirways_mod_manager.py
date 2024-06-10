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
lj.debug('current loggerjava ver:' + lj.ver, pos='test_loggerjava')
mod_database_loc = r'.\MiniAirways_mod_manager_database.json'
mod_database = {}
db_name = []
db_filename = []
db_dependencies = []
db_stat = []
basemoddic = r'.\BepInEx\plugins\\'
ver = '0.0.2'

try:
    class Database:
        def __init__(self):
            self.database = {}
            self.db_name = []
            self.db_filename = []
            self.db_dependencies = []
            self.db_stat = []

        def refreshdb(self):
            new_db = {}
            for index, data in self.database.items():
                new_db['mod' + str(len(new_db))] = data
            self.database = new_db

            self.db_name = []
            self.db_filename = []
            self.db_dependencies = []
            self.db_stat = []
            for i in range(len(self.database)):
                self.db_name.append(mod_database['mod' + str(i)]["name"])
                self.db_filename.append(mod_database['mod' + str(i)]["file_name"])
                self.db_dependencies.append(mod_database['mod' + str(i)]["dependencies"])
                self.db_stat.append(mod_database['mod' + str(i)]['active'])

        def delitem(self, index):
            self.database.pop('mod' + str(index))
            self.refreshdb()


    def loaddatabase():
        global mod_database
        try:
            if os.path.exists(mod_database_loc):
                with open(mod_database_loc, 'r') as f1:
                    mod_database = json.load(f1)
                    lj.debug(txt='read database:\n' +
                                 json.dumps(mod_database, ensure_ascii=True, indent=4, sort_keys=False),
                             pos='main.loaddatabase')
                for i in range(len(mod_database)):
                    db_name.append(mod_database['mod' + str(i)]["name"])
                    db_filename.append(mod_database['mod' + str(i)]["file_name"])
                    db_dependencies.append(mod_database['mod' + str(i)]["dependencies"])
                    db_stat.append(mod_database['mod' + str(i)]['active'])
            else:
                with open(mod_database_loc, 'x+'):
                    pass
                print('database not exist, creating a new one')
                mod_database = {}
                lj.warn('no database read', pos='main.loaddatabase')
        except JSONDecodeError:
            print("error while decoding the database")
            print("please del the database and reopen the program!")
            os.system("pause")
            exit(10)


    def refresh_exist_mods():
        global mod_database

        for filename in os.listdir(basemoddic):
            if os.path.isfile(os.path.join(basemoddic, filename)):

                base, ext = os.path.splitext(filename)

                while ext and base.count('.') > 0:
                    base, new_ext = os.path.splitext(base)
                    ext = new_ext + ext

                if (base + '.dll') not in db_filename:
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

                    if ext != ".dll.disable":
                        mod_database['mod' + str(db_filename.index(base + '.dll'))]['active'] = "True"
                    else:
                        mod_database['mod' + str(db_filename.index(base + '.dll'))]['active'] = "False"
        resort_db()
        print("loaded mods from disc!")


    def refresh_mod_status():
        global mod_database
        resort_db()
        for i in db_filename:
            if os.path.exists(basemoddic + i):
                mod_database['mod' + str(db_filename.index(i))]["active"] = "True"
            elif os.path.exists(basemoddic + i + '.disabled'):
                mod_database['mod' + str(db_filename.index(i))]['active'] = 'False'
            else:
                print("mod does not exist, deleting related data.")
                mod_database.pop('mod' + str(db_filename.index(i)))
        resort_db()
        print('refreshed database!')


    def addmod(fileroute):
        global mod_database
        resort_db()
        with zipfile.ZipFile(fileroute) as zipfile_obj:
            with zipfile_obj.open('meta-inf.json') as zip_f:
                content = zip_f.read()

                if isinstance(content, bytes):
                    content = content.decode('utf-8')

                data = json.loads(content)
        print('read mod name:%s' % data['name'])
        print('read mod description:%s' % data['desc'])
        choice = input('Continue adding procedure?(Y/N):')
        if choice != 'Y':
            print('add aborted!')
            return

        if data['file_name'] in db_filename:
            print("mod exist!")
            return
        if data['dependencies']:
            for i in data['dependencies']:
                if i == 0:
                    pass
                if i['file'] in db_filename:
                    status = mod_database['mod' + str(db_filename.index(i['file']))]['status']
                    if status != "True":
                        print("the dependence mod:%s is not activated, auto active the mod")
                        enablemod(db_filename.index(i['file']))
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

        dependened = []
        for i in db_dependencies:
            if i == 0:
                continue
            for j in i:
                if (j['name'] == mod_database['mod' + str(index)]['name'] and
                        db_stat[db_dependencies.index(i)] == 'True'):
                    dependened.append(mod_database['mod' + str(db_dependencies.index(i))]['name'])
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

        passtest = True
        if mod_database['mod' + str(index)]['dependencies']:
            for i in mod_database['mod' + str(index)]['dependencies']:
                if i['file'] in db_filename:
                    if db_stat[db_filename.index(i['file'])] != "True":
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

        dependened = []
        for i in db_dependencies:
            if i == 0:
                continue
            for j in i:
                if (j['name'] == mod_database['mod' + str(index)]['name'] and
                        db_stat[db_dependencies.index(i)] == 'True'):
                    dependened.append(mod_database['mod' + str(db_dependencies.index(i))]['name'])
        if dependened:
            print('the mod %s is dependented by mod %s!\nplease diable them before disabling!' % (
                mod_database['mod' + str(index)]['name'], dependened))
            return

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
        global mod_database, db_name, db_filename, db_dependencies, db_stat
        new_db = {}
        for index, data in mod_database.items():
            new_db['mod' + str(len(new_db))] = data
        mod_database = new_db
        db_name = []
        db_filename = []
        db_stat = []
        db_dependencies = []

        for i in range(len(mod_database)):
            db_name.append(mod_database['mod' + str(i)]["name"])
            db_filename.append(mod_database['mod' + str(i)]["file_name"])
            db_dependencies.append(mod_database['mod' + str(i)]["dependencies"])
            db_stat.append(mod_database['mod' + str(i)]['active'])


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
    refresh_exist_mods()
    refresh_mod_status()
    resort_db()

    print('Mini Airways Mod manager %s on %s' % (ver, platform.system()))
    print('Type "help" for command usages')

    # TODO: diff ver compact

    while True:
        commandd = input('[bs] ')
        commandlist = commandd.split(' ')
        command = commandlist[0]
        lj.info('user choice:' + command)
        if command == 'addmod':
            if len(commandlist) == 1:
                route = input('input the path of your downloaded mod zip file location:')
                addmod(route)
            else:
                addmod(commandd[1])
        elif command == 'disablemod':
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

rungame:
run the game!

help:
show all the usages of the commands

exit:
exit the program and save the database
            """)
    print("saving database")
    lj.info('saving db:\n' + json.dumps(mod_database, ensure_ascii=True, indent=4, sort_keys=False))
    with open(mod_database_loc, mode='w') as f:
        json.dump(mod_database, f, ensure_ascii=False, indent=4)
    lj.info('closing')
    os.system("pause")
except Exception as E:
    lj.warn(lj.handler(E), pos='exechandler', showinconsole=True)
    lj.info('db:\n' + json.dumps(mod_database, ensure_ascii=True, indent=4, sort_keys=False), pos='exechandler')
    lj.info('ver: %s os: %s' % (ver, platform.system()), pos='exechandler')
    os.system('pause')

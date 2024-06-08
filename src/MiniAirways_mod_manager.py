import json
import os
import zipfile
import platform

import loggerjava as lj

if __name__ == "__main__":
    pass

try:
    lj.config(name='MiniAirways_mod_manager_log')
    mod_database_loc = r'.\MiniAirways_mod_manager_database.json'
    mod_database = {}
    basemoddic = r'.\BepInEx\plugins\\'
    ver = '0.0.1.dev'


    def loaddatabase():
        global mod_database
        if os.path.exists(mod_database_loc):
            with open(mod_database_loc,'r') as f:
                mod_database = json.load(f)
        else:
            with open(mod_database_loc,'x+') as f:
                pass
            print('database not exist, creating a new one')
            mod_database = {}



    def refresh_exist_mods():
        global mod_database
        file_db = []
        for i in range(len(mod_database)):
            file_db.append(mod_database['mod' + str(i)]["file_name"])

        for filename in os.listdir(basemoddic):
            if os.path.isfile(os.path.join(basemoddic, filename)):
                # files.append(filename)

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
                    mod_index = file_db.index(base + '.dll')
                    if ext != ".dll.disable":
                        mod_database['mod' + str(mod_index)]['active'] = "True"
                    else:
                        mod_database['mod' + str(mod_index)]['active'] = "False"

        print("loaded mods from disc!")


    def refresh_mod_status():
        global mod_database
        resort_db()
        for i in range(len(mod_database)):
            listmod = mod_database['mod'+str(i)]
            if os.path.exists(basemoddic+listmod["file_name"]):
                mod_database['mod'+str(i)]["active"] = "True"
            elif os.path.exists(basemoddic+listmod['file_name']+'.disabled'):
                mod_database['mod'+str(i)]['active'] = 'False'
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
        print('read mod name:%s'%data['name'])
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
        for i in data['dependencies']:
            if i == 0:
                pass
            if i['file'] in file_db:
                pass
            else:
                print("the dependence mod:%s does not exist.\nplease install it before installing %s!"
                      %(i['name'],data['name']))
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
        # TODO:dependencies
        global mod_database
        print('mod to be deleted:'+mod_database['mod'+str(index)])
        confirm = input('input "Confirm" to confirm the deletion of the mod:')
        if confirm != "Confirm":
            print("confirmation aborted!")
            return
        filedir = mod_database['mod' + str(index)]['file_name']
        dll_file_path = r'.\BepInEx\plugins\\' + filedir
        if os.path.exists(dll_file_path):
            os.remove(dll_file_path)
            print(f"Mod file file {dll_file_path} has been deleted.")
        elif os.path.exists(dll_file_path+".disabled"):
            os.remove(dll_file_path)
            print(f"Mod file file {dll_file_path}.disabled has been deleted.")
        else:
            print(f"Mod file {dll_file_path} does not exist.\n"
                  f"removing the related mod data")
        mod_database.pop('mod' + str(index))
        resort_db()
        print("deleted!")


    def disablemod(index):
        # TODO:find dependence and warn
        global mod_database
        filedir = mod_database['mod' + str(index)]['filename']
        # dependences
        file_db = []
        status_db = []
        for i in range(len(mod_database)):
            file_db.append(mod_database['mod' + str(i)]["dependencies"])
            file_db.append(mod_database['mod' + str(i)]["active"])

        if file_db:#change
            print('the mod %s is dependented by mod %s!\nplease ')

        #
        if mod_database['mod' + str(index)]['active'] != "True":
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\n aborting and refreshing... ")
            refresh_exist_mods()
        if not os.path.exists(filedir):
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\n aborting and refreshing... ")
            mod_database['mod' + str(index)]['active'] = "False"
            refresh_exist_mods()
        os.rename(basemoddic + filedir, basemoddic + filedir + '.disabled')
        mod_database['mod' + str(index)]['active'] = "False"
        print("changed mod " + mod_database['mod' + str(index)]['name'] + ' status has changed to disabled')


    def enablemod(index):
        # TODO: dependencies
        global mod_database
        filedir = mod_database['mod' + str(index)]['filename']
        if mod_database['mod' + str(index)]['active'] != "False":
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\n aborting and refreshing... ")
            refresh_exist_mods()
        if not os.path.exists(filedir + '.disabled'):
            print(
                'mod ' + mod_database['mod' + str(index)]['name'] + " status is abnormal\n aborting and refreshing... ")
            mod_database['mod' + str(index)]['active'] = "False"
            refresh_exist_mods()
        os.rename(basemoddic + filedir + '.disabled', basemoddic + filedir)
        mod_database['mod' + str(index)]['active'] = "True"
        print("changed mod " + mod_database['mod' + str(index)]['name'] + ' status has changed to enabled')


    def showdesc(index):
        return mod_database['mod' + str(index)]['desc']

    def resort_db():
        global mod_database
        new_db = {}
        for index,data in mod_database.items():
            new_db['mod'+str(len(new_db))] = data
        mod_database = new_db


    loaddatabase()
    refresh_mod_status()
    refresh_exist_mods()
    resort_db()
    print('Mini Airways Mod manager %s on %s' % (ver, platform.system()))
    print('Type "help" for command usages')
    while True:
        command = input('[bs] ')
        if command == 'addmod':
            route = input('input the path of your downloaded mod zip file location:')
            addmod(route)
        # TODO: commands
        elif command == 'disablemod':
            pass
        elif command == 'enablemod':
            pass
        elif command == 'delmod':
            pass

        elif command == "showmods":
            for i in range(len(mod_database)):
                print('mod name:%s' % mod_database['mod' + str(i)]['name'])
                print('mod index:%s' % i)
                print('mod description:%s' % mod_database['mod' + str(i)]['desc'])
                # print('mod file:%s' % mod_database['mod' + str(i)]['file_name'])
                # TODO:dependencies
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
load mods from file
will automantically add mods that are not in database

help:
show all the usages of the commands

exit:
exit the program and save the database
            """)
except Exception as E:
    lj.warn(lj.handler(E))
    os.system('pause')

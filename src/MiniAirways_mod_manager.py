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
        with open(mod_database_loc) as f:
            mod_database = json.load(f)


    def output_mod_information():
        # print(mod_database)
        for i in range(len(mod_database)):
            print(mod_database['mod' + str(i)])


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
                        mod_database['mod' + str(mod_index - 1)]['active'] = "True"
                    else:
                        mod_database['mod' + str(mod_index - 1)]['active'] = "False"
            # print(files)
        # for i in files:
        #     if i not in file_db:
        #         mod_database['mod' + str(len(mod_database))] = {
        #             "name": i[:-4],
        #             "desc": "none",
        #             "file_name": i,
        #             "dependencies": 0
        #         }
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


    def addmod(fileroute):
        global mod_database
        resort_db()
        with zipfile.ZipFile(fileroute) as zipfile_obj:
            with zipfile_obj.open('meta-inf.json') as f:
                content = f.read()

                if isinstance(content, bytes):
                    content = content.decode('utf-8')

                data = json.loads(content)
        file_db = []
        for i in range(len(mod_database)):
            file_db.append(mod_database['mod' + str(i)]["file_name"])
        if data['file_name'] in file_db:
            print("mod exist!")
            return
        # TODO: find the dependencies
        # TODO: show the desc
        data['active'] = "True"

        # TODO: file name data check
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
        # TODO: confirm del
        filedir = mod_database['mod' + str(index)]['file_name']
        dll_file_path = r'.\BepInEx\plugins\\' + filedir
        if os.path.exists(dll_file_path):
            os.remove(dll_file_path)
            print(f"DLL file {dll_file_path} has been deleted.")
        else:
            print(f"DLL file {dll_file_path} does not exist.\n"
                  f"removing the related mod data")
        mod_database.pop('mod' + str(index))
        resort_db()
        print("deleted!")
        pass


    def disablemod(index):
        global mod_database
        filedir = mod_database['mod' + str(index)]['filename']
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


    """
    loaddatabase()

    # output_mod_information()
    # print(showdesc(0))
    refresh_mod_status()
    refresh_exist_mods()
    resort_db()
    # print(mod_database)
    addmod(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways Playtest\MiniAirways_mod_manager\testmod.zip')
    print(mod_database)
    index = int(input())
    delmod(index)"""
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
            
            showdescription:
            show the description of the mod
            
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

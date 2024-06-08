import json
import os
import zipfile

import loggerjava as lj

if __name__ == "__main__":
    pass

try:
    lj.config(name='MiniAirways_mod_manager_log')
    mod_database_loc = r'.\MiniAirways_mod_manager_database.json'
    mod_database = {}


    def loaddatabase():
        global mod_database
        with open(mod_database_loc) as f:
            mod_database = json.load(f)


    def output_mod_information():
        # print(mod_database)
        for i in range(len(mod_database)):
            print(mod_database['mod' + str(i)])


    # TODO: process mods


    def refresh_exist_mods():
        global mod_database
        file_db = []
        for i in range(len(mod_database)):
            file_db.append(mod_database['mod' + str(i)]["file_name"])
        dic = r'.\BepInEx\plugins\\'
        files = []
        for filename in os.listdir(dic):
            if os.path.isfile(os.path.join(dic, filename)):
                files.append(filename)
        # print(files)
        for i in files:
            if i not in file_db:
                mod_database['mod' + str(len(mod_database))] = {
                    "name": i[:-4],
                    "desc": "none",
                    "file_name": i,
                    "dependencies": 0
                }
        print("loaded mods from disc!")


    def addmod(fileroute):
        global mod_database
        with zipfile.ZipFile(fileroute) as zipfile_obj:
            with zipfile_obj.open('meta-inf.json') as f:
                content = f.read()

                if isinstance(content, bytes):
                    content = content.decode('utf-8')

                data = json.loads(content)
        # print(data)
        file_db = []
        for i in range(len(mod_database)):
            file_db.append(mod_database['mod' + str(i)]["file_name"])
        if data['file_name'] in file_db:
            print("mod exist!")
            return
        # TODO: find the dependencies
        # TODO: show the desc
        mod_database['mod' + str(len(mod_database))] = data
        with zipfile.ZipFile(fileroute, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if any(pattern in file_info.filename for pattern in ['.dll']):
                    zip_ref.extract(file_info, r'.\BepInEx\plugins\\')
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
        print("deleted!")
        pass

    def disablemod(index):
        pass

    def enablemod(index):
        pass


    def showdesc(index):
        return mod_database['mod' + str(index)]['desc']


    loaddatabase()
    # output_mod_information()
    # print(showdesc(0))
    refresh_exist_mods()
    # print(mod_database)
    addmod(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways Playtest\MiniAirways_mod_manager\testmod.zip')
    input()
    delmod(3)
except Exception as E:
    lj.warn(lj.handler(E))
    os.system('pause')

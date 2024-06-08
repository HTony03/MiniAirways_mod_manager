import json
import os

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
        print(files)
        for i in files:
            print(i in file_db)

    def addmod(file):
        global mod_database
        pass


    def delmod(index):
        global mod_database
        pass


    def showdesc(index):
        return mod_database['mod' + str(index)]['desc']

    def dllprocess(name):
        pass


    loaddatabase()
    output_mod_information()
    print(showdesc(0))
    refresh_exist_mods()
except Exception as E:
    lj.warn(lj.handler(E))
    os.system('pause')

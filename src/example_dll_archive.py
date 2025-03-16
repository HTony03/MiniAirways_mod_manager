import time
import multiprocessing
import gc

if __name__ == '__main__':pass

#from pythonnet import load
#load("coreclr")
# archive
import sys,os

sys.path.extend(r'.//ReferencedAssemblies')

import pythonnet

#pythonnet.get_runtime_info()
#clr = pythonnet.load('coreclr')
import clr
# module = clr.AddReference("VerticalLevel")
# print(module.GetName())
# print(type(module.GetName()))
# print(module.FullName)
#help(clr.AddReference("VerticalLevel"))
# Create a new AppDomain

from win32com.client import Dispatch
import json
shell = Dispatch("Shell.Application")

# enter directory where your file is located
ns = shell.NameSpace(os.path.abspath('.\\BepInEx\\'))
print(ns)
for i in ns.Items():
    # Check here with the specific filename
    base, ext = os.path.splitext(str(i))
    while ext and base.count('.') > 0:
        base, new_ext = os.path.splitext(base)
        ext = new_ext + ext
    if ext == ".dll" or ext == '.dll.disabled':
        _dict = {}
        for j in range(0,321):
            # if (ns.GetDetailsOf(i,j)
            #         and ns.GetDetailsOf(j,j) in ['Name','File description',
            #                                                      'Company','File version',
            #                                                      'Product name','Product version']\
            # ):
            _dict[ns.GetDetailsOf(j,j)] = ns.GetDetailsOf(i,j)
        for k in ['Name','File description',
                                                                 'Company','File version',
                                                                 'Product name','Product version']:

            print(list(_dict.keys()).index(k))
        _dict2 = {}
        for j in [0, 33, 34, 166, 297, 298]:
            _dict2[ns.GetDetailsOf(j, j)] = ns.GetDetailsOf(
                i, j)
        print(json.dumps( _dict2, ensure_ascii=True, indent=4, sort_keys=False))
        print(_dict)

exit()
basefolder = r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways Playtest\MiniAirways_mod_manager\src'
for filename in os.listdir(basefolder):
    if os.path.isfile(os.path.join(basefolder, filename)):

        base, ext = os.path.splitext(filename)

        while ext and base.count('.') > 0:
            base, new_ext = os.path.splitext(base)
            ext = new_ext + ext

        # print(ext)
        disabled = False
        if ext == '.dll.disabled':
            disabled = True
            os.rename(os.path.join(r'E:\PycharmProjects\MiniAirways_mod_manager\src',filename),os.path.join(r'E:\PycharmProjects\MiniAirways_mod_manager\src',base + '.dll'))
            ext = '.dll'
        if ext == '.dll':
            module = clr.AddReference(base)
            print(module.ToString().split(', ')[0])
        if ext == '.dll.disabled':
            os.rename(basefolder+'\\'+filename,basefolder+'\\'+base+'.dll')
            module = clr.AddReference(base)
            print(module.ToString().split(', ')[0])
            os.rename(basefolder+'\\'+base+'.dll',basefolder+'\\'+filename)
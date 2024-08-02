if __name__ == '__main__':pass

#from pythonnet import load
#load("coreclr")
import sys,os
sys.path.extend(r'.//ReferencedAssemblies')

import pythonnet

#pythonnet.get_runtime_info()
#clr = pythonnet.load('coreclr')
import clr
module = clr.AddReference("VerticalLevel")
print(module.GetName())
print(type(module.GetName()))
print(module.FullName)
#help(clr.AddReference("VerticalLevel"))
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
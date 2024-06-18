if __name__ == '__main__':pass

#from pythonnet import load
#load("coreclr")
import sys,os
sys.path.extend(r'.//ReferencedAssemblies')

import pythonnet

#pythonnet.get_runtime_info()
#clr = pythonnet.load('coreclr')
import clr
module = clr.AddReference("aaa")
print(module.GetName())
print(type(module.GetName()))
print(module.FullName)
print(module.GetModule)
help(clr.AddReference("VerticalLevel"))

# for filename in os.listdir(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways Playtest\MiniAirways_mod_manager\src'):
#     if os.path.isfile(os.path.join(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways Playtest\MiniAirways_mod_manager\src', filename)):
for filename in os.listdir(r'E:\PycharmProjects\MiniAirways_mod_manager\src'):
    if os.path.isfile(os.path.join(r'E:\PycharmProjects\MiniAirways_mod_manager\src',filename)):
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
            a = {}
            for i in module.ToString().split(', '):
                if '=' in i:
                    a[i.split('=')[0]] = i.split('=')[1]
                else:
                    a['name'] = i
            a['filename'] = base+'.dll'
            a.pop('Culture')
            a.pop('PublicKeyToken')
            if disabled:
                a['active'] = 'False'
            else:
                a['active'] = 'True'
            # print(a)
        if disabled:
            os.rename(os.path.join(r'E:\PycharmProjects\MiniAirways_mod_manager\src',base + '.dll'),os.path.join(r'E:\PycharmProjects\MiniAirways_mod_manager\src',filename))
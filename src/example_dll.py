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

for filename in os.listdir(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways Playtest\MiniAirways_mod_manager\src'):
    if os.path.isfile(os.path.join(r'D:\Program Files (x86)\Steam\steamapps\common\Mini Airways Playtest\MiniAirways_mod_manager\src', filename)):

        base, ext = os.path.splitext(filename)

        while ext and base.count('.') > 0:
            base, new_ext = os.path.splitext(base)
            ext = new_ext + ext

        if ext == '.dll':
            module = clr.AddReference(base)
            print(module.ToString().split(', ')[0])
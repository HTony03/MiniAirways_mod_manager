if __name__ == '__main__':pass

#from pythonnet import load
#load("coreclr")
import sys
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
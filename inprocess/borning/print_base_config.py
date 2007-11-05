import os 
from inprocess.configurations.xml_configuration import XMLConfiguration 
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration 
   
inprocessdir = __import__('inprocess').__path__[0] 
baseconfig_path = os.path.join(inprocessdir, 'configurations', 'projects', 'urbansim', 'baseline.xml') 
new = XMLConfiguration(baseconfig_path) 
old = AbstractUrbansimConfiguration() 
print new


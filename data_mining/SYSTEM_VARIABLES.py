import os, sys
from opus_core import paths

#FOR PLATFORM                                                                                                                          
#If windows set to backslash  
WIN = True
try :
    sys.getwindowsversion() #@UndefinedVariable
except AttributeError :
    WIN = False

FOLDER_TYPE = "\\"
if not WIN :
    FOLDER_TYPE = "/"

    
#loads system variables
path = paths.get_opus_home_path("src", "data_mining")

#System variables

#for outlier detection
BINARY = ""
if WIN :
    BINARY = os.path.join(path, 'models', 'WinLOF.exe')
else :
    BINARY = os.path.join(path, 'models', 'knn_binary_mac')

#FOR OUTPUT
#Prints what is happening with the test
PROFILING = True

#Draws a picture of the training and test blocks (if pygame is installed)
DRAW_BLOCKS = False

#If windows set to false
USE_SCALE = False


#FOR DATABASE
ROUND_BORDERS = True
NUMBER_DIGITS_ROUND = 3

#FOR GUI
USING_GUI = True

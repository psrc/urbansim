import os

#FOR PLATFORM                                                                                                                          
#If windows set to backslash  
WIN = True
if os.name == 'posix' :
    WIN = False


FOLDER_TYPE = "\\"
if not WIN :
    FOLDER_TYPE = "/"

    
#loads system variables
path = os.environ.get('OPUS_HOME')
path += FOLDER_TYPE + "src" + FOLDER_TYPE + "data_mining" + FOLDER_TYPE


#System variables

#for outlier detection
BINARY = path + 'models\WinLOF.exe'
if not WIN :
    BINARY = path + 'models/knn_binary_mac'

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

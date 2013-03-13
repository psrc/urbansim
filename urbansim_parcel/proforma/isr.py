import psycopg2
import os
from opus_core import paths
import cPickle

RESFEE = 1000 # per unit
NONRESFEE = 2.50 # per sqft

class ISR:

    def __init__(my):
        my.isr = cPickle.load(open(os.path.join(paths.get_opus_data_path_path(),'bay_area_parcel','isr.jar')))

    def res_isr_fee(my,taz):
        if taz == 0: return 0
        z = my.isr[taz][1]
        if z == "A": return 0
        elif z == "B": return 125 #12500
        elif z == "C": return 250 #25000
        elif z == "D": return 500 #50000
        elif z == "No Fee": return -40000
        print z
        return 0
    
    def nonres_isr_fee(my,taz):
        if taz == 0: return 0
        z = my.isr[taz][0]
        if z == "A": return 0
        elif z == "B": return 2 #5
        elif z == "C": return 7 #10
        elif z == "D": return 15 #20
        elif z == "No Fee": return -15
        print z
        return 0
import psycopg2
import os

RESFEE = 1000 # per unit
NONRESFEE = 2.50 # per sqft

class ISR:

    def __init__(my):
        passwd = os.environ['OPUS_DBPASS']
        conn_string = "host='paris.urbansim.org' dbname='bayarea' user='urbanvision' password='%s'"%passwd
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        s = "select avg(vmt_per_person_smoothed), stddev(vmt_per_person_smoothed), avg(vmt_per_worker_smoothed), stddev(vmt_per_worker_smoothed) from vmt2010"
        cursor.execute(s)
        avg_per_person, dev_per_person, avg_per_worker, dev_per_worker = \
            cursor.fetchone()

        s = "select taz, vmt_per_person_smoothed, vmt_per_worker_smoothed from vmt2010"
       
        print s 
        cursor.execute(s)
        records = cursor.fetchall()
        d = {}
        for r in records:
            taz, vmtperson, vmtworker = r
            d[taz] = [(vmtperson-avg_per_person)/dev_per_person, \
                      (vmtworker-avg_per_worker)/dev_per_worker]

        my.isr = d

    def res_isr_fee(my,taz):
        stddev = my.isr[taz][0]
        if stddev < 0: return 0
        elif stddev < 1: return 5000
        elif stddev < 2: return 15000
        elif stddev < 3: return 25000
        else: return 50000
        #return stddev * RESFEE
    
    def nonres_isr_fee(my,taz):
        stddev = my.isr[taz][1]
        if stddev < 0: return 0
        elif stddev < 1: return 2
        elif stddev < 2: return 6
        elif stddev < 3: return 10
        else: return 20
        #return stddev * NONRESFEE

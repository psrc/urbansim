import psycopg2
import os
from opus_core import paths
import cPickle

class ParcelFees:

    def __init__(my,fee_dataset):
        my.fee_dataset = fee_dataset

    def resmf_parcel_fee(my,parcel_id):
        return my.fee_dataset['cs_rr'][parcel_id]
    
    def resother_parcel_fee(my,parcel_id):
        return my.fee_dataset['cs_ro'][parcel_id]
    
    def nonres_parcel_fee(my,parcel_id):
        return my.fee_dataset['cs_nr'][parcel_id]

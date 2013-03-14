# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

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

    def get(my,pid):
        return (my.resmf_parcel_fee(pid),my.resother_parcel_fee(pid),my.nonres_parcel_fee(pid))

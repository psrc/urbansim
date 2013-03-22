# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

"""
read 30-year demographic data prepared by INED
"""

import h5py
import sys, os
import numpy as np
from subprocess import Popen, PIPE
from opus_core.logger import logger


def read_header(in_fname, rename_attrs=None, dtypes=None):
    in_fh = file(in_fname)
    header = in_fh.readline().strip().split(",")
    names = [v.lower() for v in header]
    if rename_attrs is not None:
        for org_attr, new_attr in rename_attrs.iteritems():
            names[names.index(org_attr)] = new_attr
    if dtypes is None:
        formats = ['i4'] * len(names)
    else:
        assert len(dtypes) == len(names)
        formats = dtypes
    dtype = {'names': names, 'formats':formats}
    return names, dtype

def determine_dims(in_fname):
    names, dtype = read_header(in_fname)
    ncols = len(names)
    nrows = int(Popen(["wc", "-l", in_fname], stdout=PIPE).communicate()[0].split()[0])
    ## exclude header
    nrows = nrows - 1
    return nrows, ncols

def read_csv_native(in_fname, skiprows=1, delimiter=",", comments="#"):
    names, dtype = read_header(in_fname)
    shape = determine_dims(in_fname)
    ## this may produce a MemoryError
    data = np.empty(shape=shape, dtype=dtype)
    with open(in_fname, 'U') as fh:
        for irow, row in enumerate(fh.readline()):
            if irow < skiprows: continue
            row = row.split(comments)[0].strip()
            vals = [int(val) for val in row.split(delimiter)]
            data[irow, ] = vals
    return data

 
## read csv with np.loadtxt
def read_csv_with_numpy(in_fname):
    _, dtype = read_header(in_fname)
    data = np.loadtxt(in_fname, dtype=dtype,
                      skiprows=1, delimiter=",")
    return data

def read_native_write_h5py(in_fnamel, out_fname, dataset_name, 
                           skiprows=1, delimiter=",", comments="#",
                          rename_and_fix_attrs=None):
    logger.log_note('Importing %s' % dataset_name)
    names, dtype = read_header(in_fnamel[0], rename_attrs=rename_and_fix_attrs)

    shape = determine_dims(in_fnamel[0])

    out_fh = h5py.File(out_fname)
    h5data = out_fh.create_dataset(dataset_name, shape=(shape[0],), dtype=dtype, 
                                   compression='gzip', compression_opts=5)
    
    GAP = 10000000
    
    for i, in_fname in enumerate(in_fnamel):
        with open(in_fname, 'U') as fh:
            logger.log_note('Processing %s' % in_fnamel)
            for irow, row in enumerate(fh):
                if irow < skiprows: continue
                
                if irow % 1e4 == 0:
                    logger.log_note('Processed %d/%d rows' % (irow, shape[0]))
    
                row = row.split(comments)[0].strip()
                if row == '': continue
                vals = [int(val) for val in row.split(delimiter)]
                
                maxdelta = dict( (names.index(n), vals[names.index(n)]) for n in rename_and_fix_attrs.values())

                # Adjust those attributes in rename_and_fix_attrs
                # by the respective value of the first record
                if irow == skiprows:
                    delta = dict( (n, GAP * i - maxdelta[n]) for n in maxdelta.keys())
                    logger.log_note('Adjusting IDs: %s' % delta)
                for i, d in delta.iteritems():
                    vals[i] += d
                
                h5data[irow-1] = np.array([tuple(vals)], dtype=dtype)
                
            logger.log_note('Processed %d rows in total' % (irow + 1))

    out_fh.close()
    return h5data

def usage():
    print "Usage: python %s.py chunks in_fname_hh [...] in_fname_person [...] out_fname" % sys.argv[0]
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    
    chunks = int(sys.argv[1])

    if len(sys.argv) != 3 + 2 * chunks:
        usage()
        
    in_fnames = {}
    in_fnames['household'] = sys.argv[2:(2+chunks)]
    in_fnames['person'] = sys.argv[(2+chunks):(2+2*chunks)]
    out_fname = sys.argv[2+2*chunks]

    try:
        os.unlink(out_fname)
        logger.log_note('Deleted file %s' % out_fname)
    except:
        pass

    rename_attrs = {'household': {'id':'household_id'},
                    'person':{'id':'person_id', 
                              'hh_id':'household_id'}
                    }

    for dataset_name in ('household', 'person'):
        ## read
        #data = read_csv_with_numpy(in_fname) 
        #data = read_csv_native(in_fname) 
        in_fnamel = in_fnames[dataset_name]
        data = read_native_write_h5py(in_fnamel, out_fname, dataset_name,
                                      rename_and_fix_attrs=rename_attrs[dataset_name])
        
        logger.log_note('Reorganizing %s' % dataset_name)
    
        ## post-write process
        fh = h5py.File(out_fname)
        ## re-organize hdf5 file into /<year>/household & /<year>/person
        #dataset_names = ['household', 'person']
        for year in np.unique(fh[dataset_name][:, 'year']):
            year_str = str(year)
            
            logger.log_note('Reorganizing year %s' % year_str)
    
            group = fh.get(year_str, None)
            if group is None:
                group = fh.create_group(year_str)
    
            is_year = fh[dataset_name][:, 'year'] == year
            group.create_dataset(dataset_name, data=fh[dataset_name][is_year],
                                 compression='gzip', compression_opts=5)
    
        #del fh[dataset_name]
        fh.close()

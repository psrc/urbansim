# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

"""
read 30-year demographic data prepared by INED
"""

import h5py
import sys, os
import numpy as np
from subprocess import check_output

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
    nrows = int(check_output(["wc", "-l", in_fname]).split()[0]) 
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

def read_native_write_h5py(in_fname, out_fname, dataset_name, 
                           skiprows=1, delimiter=",", comments="#",
                          rename_attrs=None):
    if rename_attrs is not None:
        rename_attrs = rename_attrs.get(dataset_name, None)
    names, dtype = read_header(in_fname, rename_attrs=rename_attrs)
    shape = determine_dims(in_fname)

    out_fh = h5py.File(out_fname)
    h5data = out_fh.create_dataset(dataset_name, shape=(shape[0],), dtype=dtype, 
                                   compression='gzip', compression_opts=9)

    with open(in_fname, 'U') as fh:
        for irow, row in enumerate(fh):
            if irow < skiprows: continue
            row = row.split(comments)[0].strip()
            if row == '': continue
            vals = [int(val) for val in row.split(delimiter)]
            h5data[irow-1] = np.array([tuple(vals)], dtype=dtype)
    out_fh.close()
    return h5data

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: python %s.py in_fname out_fname <household | person>" % sys.argv[0]
        sys.exit(0)

    in_fname, out_fname = sys.argv[1], sys.argv[2]
    dataset_name = sys.argv[3]
    assert dataset_name in ('person', 'household')
    #in_fname = 'HouseholdCensus.csv'
    #out_fname = 'households.h5'
    #dataset_name = 'household'

    ## pre-process
    ## remove the last "," from input file
    #os.system("sed 's/,\r/\r/g' -i %s" % in_fname)
    ## replace '<' with '_lt'
    #os.system("sed 's/</_lt/' -i %s" % in_fname)
    ## replace MS-DOS ctrl-Z, ie \x1a
    #os.system("sed 's/\x1a/\x20/g' -i %s" % in_fname)
    rename_attrs = {'household': {'id':'household_id'},
                    'person':{'id':'person_id', 
                              'hh_id':'household_id'}
                    }

    ## read
    #data = read_csv_with_numpy(in_fname) 
    #data = read_csv_native(in_fname) 
    data = read_native_write_h5py(in_fname, out_fname, dataset_name,
                                  rename_attrs=rename_attrs)

    ## post-write process
    fh = h5py.File(out_fname)
    ## re-organize hdf5 file into /<year>/household & /<year>/person
    #dataset_names = ['household', 'person']
    for year in np.unique(fh[dataset_name][:, 'year']):
        year_str = str(year)
        group = fh.get(year_str, None)
        if group is None:
            group = fh.create_group(year_str)

        is_year = fh[dataset_name][:, 'year'] == year
        group.create_dataset(dataset_name, data=fh[dataset_name][is_year],
                             compression='gzip', compression_opts=9)

    #del fh[dataset_name]
    fh.close()

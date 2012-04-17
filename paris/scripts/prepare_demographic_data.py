# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

"""
read 30-year demographic data prepared by INED
"""

import sys, os
import numpy as np

## read csv with np.loadtxt
def read_csv_with_numpy(in_fname):
    import numpy as np
    f = file(in_fname)
    header = f.readline().strip().split(",")
    f.close()
    names = [v.lower() for v in header]
    formats = ['i4'] * len(names)
    dtype = {'names': names, 'formats':formats}
    data = np.loadtxt(in_fname, dtype=dtype,
                      skiprows=1, delimiter=",")
    return data

## read csv with pandas.read_csv
## supposedly this would work, but it takes too much memory
#from pandas import read_csv, DataFrame, HDFStore
def read_csv_with_pandas(in_fname):
    from pandas import read_csv
    data = read_csv(in_fname, sep=",", index_col=[0,1])
    columns = [c.lower() for c in data.columns]
    data.columns = columns
    #data.set_index(['year', 'id'])
    return data


#df = DataFrame(data=data, dtype='int32')
#df.set_index(['year', 'id'])
def write_data_with_pandas(data, out_fname, dataset_name, *args, **kwargs):
    from pandas import HDFStore
    #store = HDFStore(out_fname, complib=complib, complevel=complevel)
    store = HDFStore(out_fname, *args, **kwargs)
    store[dataset_name] = data
    store.close()

"""
##read
#store = HDFStore(out_fname)
#df = store[dataset_name]
#store.close()
"""

## numpy file
#npy_fname = 'households.npy'
def write_data_with_numpy(data, out_fname, *args, **kwargs):
    import numpy as np
    np.save(out_fname, data)

"""
#data = np.load(npy_fname)
"""

## memmap isn't able to store dtype information with data
#memp_fname = 'households.memp'
def write_data_with_memmap(data, out_fname, *args, **kwargs):
    import numpy as np
    fp = np.memmap(memp_fname, dtype=data.dtype, mode='w+', shape=data.shape)
    fp[:] = data[:]
    fp.close()

"""
mp = np.memmap(memp_fname, dtype=dtype)
"""

## pytables
def write_data_with_pytables(data, out_fname, *args, **kwargs):
    import tables as tb
    ft = tb.openFile(out_fname, "w")
    #descr = dict([(n, tb.Col.from_dtype(np.dtype(t))) for n, t in zip(names, formats)])

    ## this does not work, as pytables doesn't support compound dtype
    atom = tb.Atom.from_dtype(np.dtype(dtype))
    filters = tb.Filters(complib=complib, complevel=complevel)
    hh = ft.createCArray(f.root, "households", 
                         atom=atom, 
                         shape=data.shape, 
                         filters=filters)
    hh[:] = data[:]
    ft.close()

"""
#read
ft = tb.File(out_fname, 'r')
hh = ft['households']
data = hh[:]
"""

## h5py
def write_data_with_h5py(data, out_fname, *args, **kwargs):
    import h5py
    #write
    fh = h5py.File(out_fname, 'w')
    hh = fh.create_dataset(dataset_name, shape=data.shape, dtype=data.dtype, 
                           #compression='gzip', compression_opts=9,
                           *args, **kwargs
                          )
    hh[:] = data[:]
    fh.close()

"""
#read
fh = h5py.File(out_fname, 'r')
hh = fh['households']
"""

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: python %s.py in_fname out_fname households" % sys.argv[0]
        sys.exit(0)

    in_fname, out_fname = sys.argv[1], sys.argv[2]
    dataset_name = sys.argv[3]

    #in_fname = 'HouseholdCensus.csv'
    #out_fname = 'households.h5'
    #dataset_name = 'households'

    ## remove the last "," from input file
    os.system("sed 's/,\r/\r/g' -i %s" % in_fname)

    data = read_csv_with_numpy(in_fname) 
    from pandas import DataFrame
    df = DataFrame(data=data, dtype='int32')
    df.set_index(['year', 'id'], inplace=True)
    complib, complevel = 'blosc', 9
    write_data_with_pandas(df, out_fname, dataset_name, 
                           complib=complib, complevel=complevel)


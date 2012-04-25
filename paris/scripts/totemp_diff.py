# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import sys
import numpy as np
from pandas import read_csv

sep = "\s*"
if len(sys.argv) != 3:
    print "Usage: python " + sys.argv[0] + " file1 file2"
    sys.exit(0)
f1, f2 = sys.argv[1], sys.argv[2]

v1 = read_csv(f1, sep=sep)
v2 = read_csv(f2, sep=sep)

v1 = v1.rename(columns=lambda s: s.split(':')[0])
v1 = v1.rename(columns={v1.columns[-1]:'totemp'})
v2 = v2.rename(columns=lambda s: s.split(':')[0])
v2 = v2.rename(columns={v2.columns[-1]:'target'})

id_column1 = v1.columns[0]
id_column2 = v2.columns[0]
v1.set_index(id_column1, inplace=True)
v2.set_index(id_column2, inplace=True)

v1.insert(0, 'name', v2['name'])
v1['target'] = v2[v2.columns[-1]]
v1['%diff'] = 100 * (v1['totemp'] / (v1['target']).astype('f') - 1)
rmse = np.sqrt( np.mean( (v1['totemp'] - v1['target'])**2 ) )

print v1
print
print 'rmse:', rmse

import os, sys, csv

args = sys.argv[1:]

assert len(args) == 2

rundir = args[0]
scenarionum = int(args[1])
print('BEGIN;')
for i in range(11,41):
    fname = os.path.join(rundir,'buildings-20%d.csv'%i)
    sys.stderr.write("Processing file: %s\n" % fname)
    f = csv.DictReader(open(fname))
    for r in f:
        s = """select create_building(%s,%d,%d,%s,%s,%d,cast('20%d-1-1' as TIMESTAMP),cast(NULL as TIMESTAMP));""" % (r['pid'],scenarionum,int(float(r['stories'])),r['sqft'],r['btype'],int(float(r['res_units'])),i)
        print(s)

print('COMMIT;')

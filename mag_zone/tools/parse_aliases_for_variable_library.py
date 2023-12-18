# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# Author: Jesse Ayers, MAG
# This quick and simple script is designed to generate XML records for every expression in each aliases.py file
# The XML generated can be copied and pasted into the expression library part of an XML configuration file
# TODO: write this directly into the expression library rather than temp file
# TODO: add error checking
# TODO: generalize

# datasets to loop over and create XML for
datasets = ['building',
            'business',
            'census_place',
            'county',
            'household',
            'job',
            'mpa',
            'person',
            'pseudo_blockgroup',
            'raz2012',
            'razi03',
            'taz2012',
            'tazi03',
            'zone',
            'super_raz',
            ]

# loop over each dataset and aliases.py, make appropriate string substitutions, write to txt file
def run(full_path_to_temp_file):
    # open a temporary ASCII file
    f = open(full_path_to_temp_file,'w')
    for dataset in datasets:
        cmd = 'from mag_zone.%s.aliases import aliases' % dataset
        exec(cmd)
        for alias in aliases:
            alias = alias.replace('<','&lt;')
            alias = alias.replace('>','&gt;')
            alias_list = alias.split(' = ')
            line = '<variable use="both" source="expression" name="%s.%s" type="variable_definition">%s</variable>\n' % (dataset, alias_list[0], alias_list[1])
            f.write(line)
        print('Dataset: %s complete.' % dataset)   
    f.close()


if __name__=="__main__":
    full_path_to_temp_file = 'c:/temp/xml_indicators_output.txt'
    run(full_path_to_temp_file)
    print('XML written to %s' % full_path_to_temp_file)
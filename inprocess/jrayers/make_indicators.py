#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

# script to produce a number of indicators

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.image_types.matplotlib_map import Map
from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.image_types.geotiff_map import GeotiffMap
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve
from opus_core.database_management.database_configuration import DatabaseConfiguration


'''-------------------------
   ------  SourceData ------
-------------------------------
The SourceData specifies the location of the simulation results that should be
used for computing the indicators, the years for which the indicators should be
computed, and, optionally, a second data directory for which the indicators will
be compared against. Each indicator requires a source data object to be passed
to it.
    dataset_pool_configuration:
              An object that handles which datasets get loaded and in what
              order.
    cache_directory:
              A path to the directory containing the simulation results that
              the indicators should be computed from.
    comparison_cache_directory:
              This field is optional. Set this field to the path to a second
              cache directory in order to run a cross-scenario indicator
              comparison. A subtract will be performed for equivalent
              values between scenarios.
    run_description:
              A description of this indicator batch. This field is optional.
    years:    The default years that all the indicators will be computed for.
              This field is optional, although all indicators will then need
              to have a years field.


-------------------------------
   ------  Indicators ------
-------------------------------
An indicator object specifies all the information necessary to compute
an indicator. Every indicator takes the following arguments:
    source_data:
          Data locations and years for computing the indicator.
          Described above.
    dataset_name:
          The name of the dataset that this indicator will be
          computed for.
    years:
          The years that the indicator will be computed for.
          This field is optional if the source_data object also
          has a years field. The indicator years field overrides
          the source_data years field.
    name:
          The desired name of the indicator. This field is optional.
          The default name is the indicator attribute, although
          some indicators overload the default name. Name replaces
          the old 'as' syntax.

Many of the specific indicator types require additional arguments.
The available indicator types and their additional arguments are:
--------------
Map
    A map of the indicator rendered in Matplotlib
----------------
    attribute:
        The fully qualified opus path of the indicator. If
        an expression is specified, this field is optional.
    expression:
        See below
    scale:
        A two element int list that are the min and max
        values for the scale of the outputted map.
--------------
Chart
    A chart of the data over the years rendered in Matplotlib.
    Charts should only be used when there are a small number
    of different entities (e.g. at higher levels of geographic
    aggregation).
--------------
    attribute:
        The fully qualified opus path of the indicator. If
        an expression is specified, this field is optional.
    expression:
        See below
--------------
Table
    A simple table of the indicator over each year.
--------------
    attribute:
        The fully qualified opus path of the indicator. If
        an expression is specified, this field is optional.
    expression:
        See below
    output_type:
        Tab, comma-separated output, or dbf (tab/csv/dbf).
        DBF Requires Dbfpy.

--------------
DatasetTable
    For every specified year, a tab-delimited table
    is outputted with the values of each of the
    specified attributes.
--------------
    attributes:
        List of attributes that will be computed for every year.
        Each attribute will be a column in the resulting table.
    exclude_condition:
        Determines the condition under which certain rows
        are not included in the result. This is an indicator expression.
        For example, "urbansim.gridcell.population>0".
        This field is optional.

--------------
GeotiffMap
    Uses Arcmap to generate a geotiff representation
    of the indicator. Requires ArcMap.
--------------
    package:
        The package that has the region-specific templates and
        other files needed by arcmap to generate the geotiff.
    attribute:
        The fully qualified opus path of the indicator. If
        an expression is specified, this field is optional.

--------------
ArcGeotiffMap
    A wrapper for a GeotiffMap indicator. The GeotiffMap is
    created and then ArcMap is launched and another image
    is produced. Requires ArcMap. This indicator type is no longer supported.
--------------
    package:
        The package that has the region-specific templates and
        other files needed by arcmap to generate the geotiff.
    attribute:
        The fully qualified opus path of the indicator. If
        an expression is specified, this field is optional.
    layer_file:
        Optional. Will default to ''.
    transparency:
        Optional. Will default to 0.
    exit_after_export:
        Determines if ArcMap exits after its done exporting the
        indicator. Will default to FalseOptional. Will default
        to False.
    export_type:
        The output format of the outputted indicator from ArcMap.
        Optional. Will default to jpg
'''

#An example script:

source_data = SourceData(
   cache_directory = r'C:\urbansim_cache\eugene\runs\run_4175.2007_11_26_09_26',
   comparison_cache_directory = r'',
   years = [1980],
   dataset_pool_configuration = DatasetPoolConfiguration(
         package_order=['eugene','urbansim','opus_core'],
         package_order_exceptions={},
         ),
)

indicators = [

   DatasetTable(
       source_data = source_data,
       dataset_name = 'zone',
       name = 'test_zone_Table',
       attributes = ['eugene.zones.travel_time_to_cbd'],
       output_type = 'esri',
       storage_location = 'c:/temp/test_fgdb.gdb'
   ),

   ]



if __name__ == '__main__':
    from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory

    IndicatorFactory().create_indicators(
        indicators = indicators,
        display_error_box = False,
        show_results = False)
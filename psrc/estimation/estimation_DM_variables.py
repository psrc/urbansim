# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

specification = {}


specification['residential'] = {
    1:  #sub_model
        [
#         ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#         ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#         ("urbansim.gridcell.is_near_highway","HWY"),  #
#         ("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
#         ("urbansim.gridcell.is_in_wetland","WTLND"),#
#         ("urbansim.gridcell.is_in_floodplain","FLOOD"),#
#         ("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#

        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#         ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),
#  #       ("urbansim.gridcell.total_improvement_value_within_walking_distance","IMPVW"),
           ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#        ("ln_bounded(urbansim.gridcell.total_improvement_value_per_residential_unit_within_walking_distance)","LIMPPUW"),

#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
         ("urbansim.gridcell.ln_residential_units","LDU"),
        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#          ("urbansim.gridcell.has_1_units","UNIT_1"),#
# #         ("urbansim.gridcell.has_2_units","UNIT_2"),#      
#          ("urbansim.gridcell.has_1_to_9_units","U1_9"),
#          ("urbansim.gridcell.has_10_to_49_units","U10_49"),
   #       ("urbansim.gridcell.has_1_to_3_units","UNIT_13"),
   #       ("urbansim.gridcell.has_3_to_10_units","UNIT_310"),
#           ("urbansim.gridcell.has_10_to_600_units","UNIT_10600"),
#          ("urbansim.gridcell.has_100_to_9999_units","UNIT_100M"),

    ('urbansim.gridcell.building_age', 'BLD_AGE'),

#   ('ln_bounded(urbansim.gridcell.average_income)', 'LAINC'),
           
     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

#   ('ln_bounded(urbansim.gridcell.average_income_when_has_1_unit)', 'LAINC_U1'),
#   ("ln_bounded(urbansim.gridcell.average_income_per_housing_unit)","LAINC_PU"),

#     ('urbansim.gridcell.is_average_income_high_income','HINC'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_1_to_5_units','HI1_5U'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_6_to_10_units','HI6_10U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_15_units','HIW7_22U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_6_units','HIW1_6U'),         

#    ("ln_bounded(urbansim.gridcell.average_income_when_has_1_to_5_units)",'LAINC_U15'),
#    ("ln_bounded(urbansim.gridcell.average_income_when_has_6_to_10_units)",'LAINC_U610'),

#      ("urbansim.gridcell.number_of_high_income_households_within_walking_distance",'HIW'),
#      ("urbansim.gridcell.percent_high_income_households_within_walking_distance", 'PHIW'),
        
# #         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
# #         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
# #         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
# #         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
# #         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
# #         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

         ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#      ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
#      ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
#      ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
          ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

#         ("urbansim.gridcell.is_high_income_and_70_or_higher_percent_developed_within_walking", "D70HI"),
         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
#         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),         

         ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),  
         ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),

# #         ("urbansim.gridcell.is_plan_type_11","PT_11"),   #residential_high
# #          ("urbansim.gridcell.is_plan_type_12","PT_12"),   #residential_light
# #         ("urbansim.gridcell.is_plan_type_13","PT_13"),    #residential_low
#          #("urbansim.gridcell.is_plan_type_14","PT_14"),    #residential_medium
# #         ("urbansim.gridcell.is_plan_type_15","PT_15"),   #residential_rural

#  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE40MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_40_minutes_travel_time_hbw_am_transit_walk))','LNE40MTW'),


# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
       ],

    2:  #sub_model
        [
#         ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#         ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#         ("urbansim.gridcell.is_near_highway","HWY"),  #
#         #("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
#         #("urbansim.gridcell.is_in_wetland","WTLND"),#
#         #("urbansim.gridcell.is_in_floodplain","FLOOD"),#
#         #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#

        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#         ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),
#  #       ("urbansim.gridcell.total_improvement_value_within_walking_distance","IMPVW"),
           ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#        ("ln_bounded(urbansim.gridcell.total_improvement_value_per_residential_unit_within_walking_distance)","LIMPPUW"),

#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
         ("urbansim.gridcell.ln_residential_units","LDU"),
        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#          ("urbansim.gridcell.has_1_units","UNIT_1"),#
# #         ("urbansim.gridcell.has_2_units","UNIT_2"),#      
 #         ("urbansim.gridcell.has_1_to_10_units","U1_5"),
 #         ("urbansim.gridcell.has_10_to_21_units","U10_21"),
   #       ("urbansim.gridcell.has_1_to_3_units","UNIT_13"),
   #       ("urbansim.gridcell.has_3_to_10_units","UNIT_310"),
#           ("urbansim.gridcell.has_10_to_600_units","UNIT_10600"),
#          ("urbansim.gridcell.has_1_to_10_units","UNIT_110"),

    ('urbansim.gridcell.building_age', 'BLD_AGE'),

#   ('ln_bounded(urbansim.gridcell.average_income)', 'LAINC'),
           
     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

#   ('ln_bounded(urbansim.gridcell.average_income_when_has_1_unit)', 'LAINC_U1'),
#   ("ln_bounded(urbansim.gridcell.average_income_per_housing_unit)","LAINC_PU"),

#     ('urbansim.gridcell.is_average_income_high_income','HINC'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_1_to_5_units','HI1_5U'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_6_to_10_units','HI6_10U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_15_units','HIW7_22U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_6_units','HIW1_6U'),         

#    ("ln_bounded(urbansim.gridcell.average_income_when_has_1_to_5_units)",'LAINC_U15'),
#    ("ln_bounded(urbansim.gridcell.average_income_when_has_6_to_10_units)",'LAINC_U610'),

#      ("urbansim.gridcell.number_of_high_income_households_within_walking_distance",'HIW'),
#      ("urbansim.gridcell.percent_high_income_households_within_walking_distance", 'PHIW'),
        
# #         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
# #         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
# #         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
# #         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
# #         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
# #         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

         ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#      ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
#      ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
#      ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
          ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

#         ("urbansim.gridcell.is_high_income_and_70_or_higher_percent_developed_within_walking", "D70HI"),
         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
#         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),         

         ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),
         ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),

# #         ("urbansim.gridcell.is_plan_type_11","PT_11"),   #residential_high
# #          ("urbansim.gridcell.is_plan_type_12","PT_12"),   #residential_light
# #         ("urbansim.gridcell.is_plan_type_13","PT_13"),    #residential_low
#          #("urbansim.gridcell.is_plan_type_14","PT_14"),    #residential_medium
# #         ("urbansim.gridcell.is_plan_type_15","PT_15"),   #residential_rural

#  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE40MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_40_minutes_travel_time_hbw_am_transit_walk))','LNE40MTW'),


# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
       ],

 
    3:  #sub_model
        [
#         ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#         ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#         ("urbansim.gridcell.is_near_highway","HWY"),  #
#         #("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
#         #("urbansim.gridcell.is_in_wetland","WTLND"),#
#         #("urbansim.gridcell.is_in_floodplain","FLOOD"),#
#         #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#

        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#         ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),
#  #       ("urbansim.gridcell.total_improvement_value_within_walking_distance","IMPVW"),
           ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#        ("ln_bounded(urbansim.gridcell.total_improvement_value_per_residential_unit_within_walking_distance)","LIMPPUW"),

#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
         ("urbansim.gridcell.ln_residential_units","LDU"),
        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#          ("urbansim.gridcell.has_1_units","UNIT_1"),#
# #         ("urbansim.gridcell.has_2_units","UNIT_2"),#      
 #         ("urbansim.gridcell.has_1_to_10_units","U1_5"),
 #         ("urbansim.gridcell.has_10_to_21_units","U10_21"),
   #       ("urbansim.gridcell.has_1_to_3_units","UNIT_13"),
   #       ("urbansim.gridcell.has_3_to_10_units","UNIT_310"),
#           ("urbansim.gridcell.has_10_to_600_units","UNIT_10600"),
#          ("urbansim.gridcell.has_1_to_10_units","UNIT_110"),

    ('urbansim.gridcell.building_age', 'BLD_AGE'),

#   ('ln_bounded(urbansim.gridcell.average_income)', 'LAINC'),
           
     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

#   ('ln_bounded(urbansim.gridcell.average_income_when_has_1_unit)', 'LAINC_U1'),
#   ("ln_bounded(urbansim.gridcell.average_income_per_housing_unit)","LAINC_PU"),

#     ('urbansim.gridcell.is_average_income_high_income','HINC'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_1_to_5_units','HI1_5U'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_6_to_10_units','HI6_10U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_15_units','HIW7_22U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_6_units','HIW1_6U'),         

#    ("ln_bounded(urbansim.gridcell.average_income_when_has_1_to_5_units)",'LAINC_U15'),
#    ("ln_bounded(urbansim.gridcell.average_income_when_has_6_to_10_units)",'LAINC_U610'),

#      ("urbansim.gridcell.number_of_high_income_households_within_walking_distance",'HIW'),
#      ("urbansim.gridcell.percent_high_income_households_within_walking_distance", 'PHIW'),
        
# #         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
# #         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
# #         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
# #         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
# #         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
# #         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

         ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#      ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
#      ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
#      ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
          ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

#         ("urbansim.gridcell.is_high_income_and_70_or_higher_percent_developed_within_walking", "D70HI"),
#         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
#         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),         

         ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),
         ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
    #     ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),

# #         ("urbansim.gridcell.is_plan_type_11","PT_11"),   #residential_high
# #          ("urbansim.gridcell.is_plan_type_12","PT_12"),   #residential_light
# #         ("urbansim.gridcell.is_plan_type_13","PT_13"),    #residential_low
#          #("urbansim.gridcell.is_plan_type_14","PT_14"),    #residential_medium
# #         ("urbansim.gridcell.is_plan_type_15","PT_15"),   #residential_rural

#  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE40MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_40_minutes_travel_time_hbw_am_transit_walk))','LNE40MTW'),


# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
       ],


    4:  #sub_model
        [
#         ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#         ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#         ("urbansim.gridcell.is_near_highway","HWY"),  #
#         #("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
#         #("urbansim.gridcell.is_in_wetland","WTLND"),#
#         #("urbansim.gridcell.is_in_floodplain","FLOOD"),#
#         #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#

        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#         ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),
#  #       ("urbansim.gridcell.total_improvement_value_within_walking_distance","IMPVW"),
           ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#        ("ln_bounded(urbansim.gridcell.total_improvement_value_per_residential_unit_within_walking_distance)","LIMPPUW"),

#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
         ("urbansim.gridcell.ln_residential_units","LDU"),
        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#          ("urbansim.gridcell.has_1_units","UNIT_1"),#
# #         ("urbansim.gridcell.has_2_units","UNIT_2"),#      
 #         ("urbansim.gridcell.has_1_to_10_units","U1_5"),
 #         ("urbansim.gridcell.has_10_to_21_units","U10_21"),
   #       ("urbansim.gridcell.has_1_to_3_units","UNIT_13"),
   #       ("urbansim.gridcell.has_3_to_10_units","UNIT_310"),
#           ("urbansim.gridcell.has_10_to_600_units","UNIT_10600"),
#          ("urbansim.gridcell.has_1_to_10_units","UNIT_110"),

    ('urbansim.gridcell.building_age', 'BLD_AGE'),

#   ('ln_bounded(urbansim.gridcell.average_income)', 'LAINC'),
           
#     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

#   ('ln_bounded(urbansim.gridcell.average_income_when_has_1_unit)', 'LAINC_U1'),
#   ("ln_bounded(urbansim.gridcell.average_income_per_housing_unit)","LAINC_PU"),

#     ('urbansim.gridcell.is_average_income_high_income','HINC'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_1_to_5_units','HI1_5U'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_6_to_10_units','HI6_10U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_15_units','HIW7_22U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_6_units','HIW1_6U'),         

#    ("ln_bounded(urbansim.gridcell.average_income_when_has_1_to_5_units)",'LAINC_U15'),
#    ("ln_bounded(urbansim.gridcell.average_income_when_has_6_to_10_units)",'LAINC_U610'),

#      ("urbansim.gridcell.number_of_high_income_households_within_walking_distance",'HIW'),
#      ("urbansim.gridcell.percent_high_income_households_within_walking_distance", 'PHIW'),
        
# #         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
# #         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
# #         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
# #         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
# #         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
# #         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

         ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#      ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
#      ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
#      ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
          ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

#         ("urbansim.gridcell.is_high_income_and_70_or_higher_percent_developed_within_walking", "D70HI"),
         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
#         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),         

         ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),
         ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),

# #         ("urbansim.gridcell.is_plan_type_11","PT_11"),   #residential_high
# #          ("urbansim.gridcell.is_plan_type_12","PT_12"),   #residential_light
# #         ("urbansim.gridcell.is_plan_type_13","PT_13"),    #residential_low
#          #("urbansim.gridcell.is_plan_type_14","PT_14"),    #residential_medium
# #         ("urbansim.gridcell.is_plan_type_15","PT_15"),   #residential_rural

#  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE40MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_40_minutes_travel_time_hbw_am_transit_walk))','LNE40MTW'),


# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
       ],

    5:  #sub_model
        [
#         ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#         ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#         ("urbansim.gridcell.is_near_highway","HWY"),  #
#         #("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
#         #("urbansim.gridcell.is_in_wetland","WTLND"),#
#         #("urbansim.gridcell.is_in_floodplain","FLOOD"),#
#         #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#

        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#         ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),
#  #       ("urbansim.gridcell.total_improvement_value_within_walking_distance","IMPVW"),
           ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#        ("ln_bounded(urbansim.gridcell.total_improvement_value_per_residential_unit_within_walking_distance)","LIMPPUW"),

#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
         ("urbansim.gridcell.ln_residential_units","LDU"),
        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#          ("urbansim.gridcell.has_1_units","UNIT_1"),#
# #         ("urbansim.gridcell.has_2_units","UNIT_2"),#      
 #         ("urbansim.gridcell.has_1_to_10_units","U1_5"),
 #         ("urbansim.gridcell.has_10_to_21_units","U10_21"),
   #       ("urbansim.gridcell.has_1_to_3_units","UNIT_13"),
   #       ("urbansim.gridcell.has_3_to_10_units","UNIT_310"),
#           ("urbansim.gridcell.has_10_to_600_units","UNIT_10600"),
#          ("urbansim.gridcell.has_1_to_10_units","UNIT_110"),

    ('urbansim.gridcell.building_age', 'BLD_AGE'),

#   ('ln_bounded(urbansim.gridcell.average_income)', 'LAINC'),
           
#     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

#   ('ln_bounded(urbansim.gridcell.average_income_when_has_1_unit)', 'LAINC_U1'),
#   ("ln_bounded(urbansim.gridcell.average_income_per_housing_unit)","LAINC_PU"),

#     ('urbansim.gridcell.is_average_income_high_income','HINC'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_1_to_5_units','HI1_5U'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_6_to_10_units','HI6_10U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_15_units','HIW7_22U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_6_units','HIW1_6U'),         

#    ("ln_bounded(urbansim.gridcell.average_income_when_has_1_to_5_units)",'LAINC_U15'),
#    ("ln_bounded(urbansim.gridcell.average_income_when_has_6_to_10_units)",'LAINC_U610'),

#      ("urbansim.gridcell.number_of_high_income_households_within_walking_distance",'HIW'),
#      ("urbansim.gridcell.percent_high_income_households_within_walking_distance", 'PHIW'),
        
# #         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
# #         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
# #         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
# #         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
# #         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
# #         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

         ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#      ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
#      ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
#      ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
          ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

#         ("urbansim.gridcell.is_high_income_and_70_or_higher_percent_developed_within_walking", "D70HI"),
         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
#         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),         

         ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),
         ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),

# #         ("urbansim.gridcell.is_plan_type_11","PT_11"),   #residential_high
# #          ("urbansim.gridcell.is_plan_type_12","PT_12"),   #residential_light
# #         ("urbansim.gridcell.is_plan_type_13","PT_13"),    #residential_low
#          #("urbansim.gridcell.is_plan_type_14","PT_14"),    #residential_medium
# #         ("urbansim.gridcell.is_plan_type_15","PT_15"),   #residential_rural

#  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE40MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_40_minutes_travel_time_hbw_am_transit_walk))','LNE40MTW'),


# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
       ],


    6:  #sub_model
        [
#         ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#         ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#         ("urbansim.gridcell.is_near_highway","HWY"),  #
#         #("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
#         #("urbansim.gridcell.is_in_wetland","WTLND"),#
#         #("urbansim.gridcell.is_in_floodplain","FLOOD"),#
#         #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#

        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#         ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),
#  #       ("urbansim.gridcell.total_improvement_value_within_walking_distance","IMPVW"),
           ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#        ("ln_bounded(urbansim.gridcell.total_improvement_value_per_residential_unit_within_walking_distance)","LIMPPUW"),

#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
         ("urbansim.gridcell.ln_residential_units","LDU"),
        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#          ("urbansim.gridcell.has_1_units","UNIT_1"),#
# #         ("urbansim.gridcell.has_2_units","UNIT_2"),#      
 #         ("urbansim.gridcell.has_1_to_10_units","U1_5"),
 #         ("urbansim.gridcell.has_10_to_21_units","U10_21"),
   #       ("urbansim.gridcell.has_1_to_3_units","UNIT_13"),
   #       ("urbansim.gridcell.has_3_to_10_units","UNIT_310"),
#           ("urbansim.gridcell.has_10_to_600_units","UNIT_10600"),
#          ("urbansim.gridcell.has_1_to_10_units","UNIT_110"),

    ('urbansim.gridcell.building_age', 'BLD_AGE'),

#   ('ln_bounded(urbansim.gridcell.average_income)', 'LAINC'),
           
#     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

#   ('ln_bounded(urbansim.gridcell.average_income_when_has_1_unit)', 'LAINC_U1'),
#   ("ln_bounded(urbansim.gridcell.average_income_per_housing_unit)","LAINC_PU"),

#     ('urbansim.gridcell.is_average_income_high_income','HINC'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_1_to_5_units','HI1_5U'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_6_to_10_units','HI6_10U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_15_units','HIW7_22U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_6_units','HIW1_6U'),         

#    ("ln_bounded(urbansim.gridcell.average_income_when_has_1_to_5_units)",'LAINC_U15'),
#    ("ln_bounded(urbansim.gridcell.average_income_when_has_6_to_10_units)",'LAINC_U610'),

#      ("urbansim.gridcell.number_of_high_income_households_within_walking_distance",'HIW'),
#      ("urbansim.gridcell.percent_high_income_households_within_walking_distance", 'PHIW'),
        
# #         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
# #         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
# #         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
# #         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
# #         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
# #         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

         ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#      ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
#      ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
#      ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
#          ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

#         ("urbansim.gridcell.is_high_income_and_70_or_higher_percent_developed_within_walking", "D70HI"),
         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
#         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),         

         ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),
         ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),

# #         ("urbansim.gridcell.is_plan_type_11","PT_11"),   #residential_high
# #          ("urbansim.gridcell.is_plan_type_12","PT_12"),   #residential_light
# #         ("urbansim.gridcell.is_plan_type_13","PT_13"),    #residential_low
#          #("urbansim.gridcell.is_plan_type_14","PT_14"),    #residential_medium
# #         ("urbansim.gridcell.is_plan_type_15","PT_15"),   #residential_rural

#  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE40MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_40_minutes_travel_time_hbw_am_transit_walk))','LNE40MTW'),


# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
       ],

    7:  #sub_model
        [
#         ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#         ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#         ("urbansim.gridcell.is_near_highway","HWY"),  #
#         #("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
#         #("urbansim.gridcell.is_in_wetland","WTLND"),#
#         #("urbansim.gridcell.is_in_floodplain","FLOOD"),#
#         #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#

        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#         ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),
#  #       ("urbansim.gridcell.total_improvement_value_within_walking_distance","IMPVW"),
           ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#        ("ln_bounded(urbansim.gridcell.total_improvement_value_per_residential_unit_within_walking_distance)","LIMPPUW"),

#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
         ("urbansim.gridcell.ln_residential_units","LDU"),
        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#          ("urbansim.gridcell.has_1_units","UNIT_1"),#
# #         ("urbansim.gridcell.has_2_units","UNIT_2"),#      
 #         ("urbansim.gridcell.has_1_to_10_units","U1_5"),
 #         ("urbansim.gridcell.has_10_to_21_units","U10_21"),
   #       ("urbansim.gridcell.has_1_to_3_units","UNIT_13"),
   #       ("urbansim.gridcell.has_3_to_10_units","UNIT_310"),
#           ("urbansim.gridcell.has_10_to_600_units","UNIT_10600"),
#          ("urbansim.gridcell.has_1_to_10_units","UNIT_110"),

    ('urbansim.gridcell.building_age', 'BLD_AGE'),

#   ('ln_bounded(urbansim.gridcell.average_income)', 'LAINC'),
           
#     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

#   ('ln_bounded(urbansim.gridcell.average_income_when_has_1_unit)', 'LAINC_U1'),
#   ("ln_bounded(urbansim.gridcell.average_income_per_housing_unit)","LAINC_PU"),

#     ('urbansim.gridcell.is_average_income_high_income','HINC'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_1_to_5_units','HI1_5U'),
#    ('urbansim.gridcell.is_average_income_high_income_and_has_6_to_10_units','HI6_10U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_15_units','HIW7_22U'),
#    ('urbansim.gridcell.is_average_income_within_walking_distance_high_income_and_has_1_to_6_units','HIW1_6U'),         

#    ("ln_bounded(urbansim.gridcell.average_income_when_has_1_to_5_units)",'LAINC_U15'),
#    ("ln_bounded(urbansim.gridcell.average_income_when_has_6_to_10_units)",'LAINC_U610'),

#      ("urbansim.gridcell.number_of_high_income_households_within_walking_distance",'HIW'),
#      ("urbansim.gridcell.percent_high_income_households_within_walking_distance", 'PHIW'),
        
# #         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
# #         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
# #         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
# #         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
# #         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
# #         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

#         ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#      ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
#      ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
#      ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
#          ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

#         ("urbansim.gridcell.is_high_income_and_70_or_higher_percent_developed_within_walking", "D70HI"),
#         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
#         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),         

         ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),
         ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
#   #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#   #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),

# #         ("urbansim.gridcell.is_plan_type_11","PT_11"),   #residential_high
# #          ("urbansim.gridcell.is_plan_type_12","PT_12"),   #residential_light
# #         ("urbansim.gridcell.is_plan_type_13","PT_13"),    #residential_low
#          #("urbansim.gridcell.is_plan_type_14","PT_14"),    #residential_medium
# #         ("urbansim.gridcell.is_plan_type_15","PT_15"),   #residential_rural

#  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE40MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_40_minutes_travel_time_hbw_am_transit_walk))','LNE40MTW'),


# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
       ],
    }


######################### commercial #########################    
specification['commercial'] = { #commercial
    1:  #sub_model
        [
#       ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#       ("urbansim.gridcell.ln_distance_to_arterial","LDART"), #variable name, coefficient name       
       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name       
       ("urbansim.gridcell.is_near_highway","HWY"),  #
#      ("urbansim.gridcell.ln_distance_to_highway","LDHWY"),  #
        #("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
        #("urbansim.gridcell.is_in_wetland","WTLND"),#
        #("urbansim.gridcell.is_in_floodplain","FLOOD"),#
        #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#
     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

 #      ("urbansim.gridcell.ln_total_value","LV"),
     ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),         
         ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
 #       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
        
#         ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
        ("urbansim.gridcell.ln_residential_units","LDU"),
         ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#         ("urbansim.gridcell.has_1_units","UNIT_1"),#
#         ("urbansim.gridcell.has_2_units","UNIT_2"),#
#         ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#

         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
          ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#          ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

#    ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
          ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDEV"),
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),
         ("urbansim.gridcell.n_commercial_sqft_recently_added_within_walking_distance", "RCSFW"),
          
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  

#         ("urbansim.gridcell.is_plan_type_2","PT_2"),   #commercial
#         ("urbansim.gridcell.is_plan_type_3","PT_3"),    #commercial_low
  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE30MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))','LNE30MTW'),
  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
 ],
    
    2:  #sub_model
        [
#       ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#       ("urbansim.gridcell.ln_distance_to_arterial","LDART"), #variable name, coefficient name       
       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name       
       ("urbansim.gridcell.is_near_highway","HWY"),  #
#      ("urbansim.gridcell.ln_distance_to_highway","LDHWY"),  #
        #("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
        #("urbansim.gridcell.is_in_wetland","WTLND"),#
        #("urbansim.gridcell.is_in_floodplain","FLOOD"),#
        #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#
     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

 #      ("urbansim.gridcell.ln_total_value","LV"),
     ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),         
         ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
 #       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
        
#         ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
        ("urbansim.gridcell.ln_residential_units","LDU"),
         ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#         ("urbansim.gridcell.has_1_units","UNIT_1"),#
#         ("urbansim.gridcell.has_2_units","UNIT_2"),#
#         ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#

         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
          ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#          ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

#    ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
#    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#          ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDEV"),
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),
         ("urbansim.gridcell.n_commercial_sqft_recently_added_within_walking_distance", "RCSFW"),
          
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  

#         ("urbansim.gridcell.is_plan_type_2","PT_2"),   #commercial
#         ("urbansim.gridcell.is_plan_type_3","PT_3"),    #commercial_low
  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE30MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))','LNE30MTW'),
  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
 ],
    
    3:  #sub_model
        [
#       ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#       ("urbansim.gridcell.ln_distance_to_arterial","LDART"), #variable name, coefficient name       
       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name       
       ("urbansim.gridcell.is_near_highway","HWY"),  #
#      ("urbansim.gridcell.ln_distance_to_highway","LDHWY"),  #
        #("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
        #("urbansim.gridcell.is_in_wetland","WTLND"),#
        #("urbansim.gridcell.is_in_floodplain","FLOOD"),#
        #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#
     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

 #      ("urbansim.gridcell.ln_total_value","LV"),
     ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),         
         ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
 #       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
        
#         ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#         ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#         ("urbansim.gridcell.has_1_units","UNIT_1"),#
#         ("urbansim.gridcell.has_2_units","UNIT_2"),#
#         ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#

         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
#          ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#          ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

#    ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
#    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
          ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDEV"),
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),
#         ("urbansim.gridcell.n_commercial_sqft_recently_added_within_walking_distance", "RCSFW"),
          
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  

#         ("urbansim.gridcell.is_plan_type_2","PT_2"),   #commercial
#         ("urbansim.gridcell.is_plan_type_3","PT_3"),    #commercial_low
  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE30MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))','LNE30MTW'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
 ],
    
    4:  #sub_model
        [
#       ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#       ("urbansim.gridcell.ln_distance_to_arterial","LDART"), #variable name, coefficient name       
#       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name       
#       ("urbansim.gridcell.is_near_highway","HWY"),  #
#      ("urbansim.gridcell.ln_distance_to_highway","LDHWY"),  #
        #("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
        #("urbansim.gridcell.is_in_wetland","WTLND"),#
        #("urbansim.gridcell.is_in_floodplain","FLOOD"),#
        #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#
     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

 #      ("urbansim.gridcell.ln_total_value","LV"),
     ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),         
         ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
 #       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
        
#         ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
#        ("urbansim.gridcell.ln_residential_units","LDU"),
         ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#         ("urbansim.gridcell.has_1_units","UNIT_1"),#
#         ("urbansim.gridcell.has_2_units","UNIT_2"),#
#         ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#

         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
          ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#          ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

#    ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
#    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
          ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDEV"),
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),
         ("urbansim.gridcell.n_commercial_sqft_recently_added_within_walking_distance", "RCSFW"),
          
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  

#         ("urbansim.gridcell.is_plan_type_2","PT_2"),   #commercial
#         ("urbansim.gridcell.is_plan_type_3","PT_3"),    #commercial_low
  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE30MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))','LNE30MTW'),
  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
 ],

    
    5:  #sub_model
        [
#       ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
#       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
#       ("urbansim.gridcell.ln_distance_to_arterial","LDART"), #variable name, coefficient name       
       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name       
#       ("urbansim.gridcell.is_near_highway","HWY"),  #
#      ("urbansim.gridcell.ln_distance_to_highway","LDHWY"),  #
        #("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
        #("urbansim.gridcell.is_in_wetland","WTLND"),#
        #("urbansim.gridcell.is_in_floodplain","FLOOD"),#
        #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#
     ("ln_bounded(urbansim.gridcell.average_income_within_walking_distance)",'LAINCW'),

 #      ("urbansim.gridcell.ln_total_value","LV"),
     ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'LIMP'),         
         ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
 #       ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
        
#         ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
        ("urbansim.gridcell.ln_residential_units","LDU"),
         ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.has_0_units","UNIT_0"),#
#         ("urbansim.gridcell.has_1_units","UNIT_1"),#
#         ("urbansim.gridcell.has_2_units","UNIT_2"),#
#         ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#

         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#         ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
#          ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#          ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#

#    ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
    
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#          ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#         ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 

#         ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"), 

         ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDEV"),
#         ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "NRDEVW"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
         ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),
         ("urbansim.gridcell.n_commercial_sqft_recently_added_within_walking_distance", "RCSFW"),
          
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  

#         ("urbansim.gridcell.is_plan_type_2","PT_2"),   #commercial
#         ("urbansim.gridcell.is_plan_type_3","PT_3"),    #commercial_low
  ('LNE30MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
  ('LNE30MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))','LNE30MTW'),
  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
 ],
    }

specification['industrial'] = { #industrial
    1:  #sub_model
        [
#       ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
       ("urbansim.gridcell.is_near_highway","HWY"),  #
#      ("urbansim.gridcell.ln_distance_to_highway","LDHWY"),
#        ("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
        #("urbansim.gridcell.is_in_wetland","WTLND"),#
#        ("urbansim.gridcell.is_in_floodplain","FLOOD"),#
        #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#
        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
        ("ln(urbansim.gridcell.average_income_within_walking_distance)","LINCW"),
#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
     #    ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
          ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
          ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#          ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDEV"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
          ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),
#         ("urbansim.gridcell.n_commercial_sqft_recently_added_within_walking_distance", "RCSFW"),
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  

  #        ("urbansim.gridcell.is_plan_type_6","PT_6"),   #industrial
#         ("urbansim.gridcell.is_plan_type_7","PT_7"),    #industrial_mix
# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
 ],

    
    2:  #sub_model
        [
#       ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
       ("urbansim.gridcell.is_near_highway","HWY"),  #
#      ("urbansim.gridcell.ln_distance_to_highway","LDHWY"),
#        ("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
        #("urbansim.gridcell.is_in_wetland","WTLND"),#
#        ("urbansim.gridcell.is_in_floodplain","FLOOD"),#
        #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#
        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
        ("ln(urbansim.gridcell.average_income_within_walking_distance)","LINCW"),
#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
     #    ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
          ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
          ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#          ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDEV"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
          ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),
#         ("urbansim.gridcell.n_commercial_sqft_recently_added_within_walking_distance", "RCSFW"),
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  

  #        ("urbansim.gridcell.is_plan_type_6","PT_6"),   #industrial
#         ("urbansim.gridcell.is_plan_type_7","PT_7"),    #industrial_mix
# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
 ],

    
    3:  #sub_model
        [
#       ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
       ("urbansim.gridcell.is_near_highway","HWY"),  #
#      ("urbansim.gridcell.ln_distance_to_highway","LDHWY"),
#        ("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
        #("urbansim.gridcell.is_in_wetland","WTLND"),#
#        ("urbansim.gridcell.is_in_floodplain","FLOOD"),#
        #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#
        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
        ("ln(urbansim.gridcell.average_income_within_walking_distance)","LINCW"),
#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
     #    ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
          ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
          ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#          ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDEV"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
          ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),
#         ("urbansim.gridcell.n_commercial_sqft_recently_added_within_walking_distance", "RCSFW"),
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  

  #        ("urbansim.gridcell.is_plan_type_6","PT_6"),   #industrial
#         ("urbansim.gridcell.is_plan_type_7","PT_7"),    #industrial_mix
# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
 ],

    
    4:  #sub_model
        [
#       ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
       ("urbansim.gridcell.is_near_highway","HWY"),  #
#      ("urbansim.gridcell.ln_distance_to_highway","LDHWY"),
#        ("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
        #("urbansim.gridcell.is_in_wetland","WTLND"),#
#        ("urbansim.gridcell.is_in_floodplain","FLOOD"),#
        #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#
        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
        ("ln(urbansim.gridcell.average_income_within_walking_distance)","LINCW"),
#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
     #    ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
          ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
          ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#          ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDEV"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
          ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),
#         ("urbansim.gridcell.n_commercial_sqft_recently_added_within_walking_distance", "RCSFW"),
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  

  #        ("urbansim.gridcell.is_plan_type_6","PT_6"),   #industrial
#         ("urbansim.gridcell.is_plan_type_7","PT_7"),    #industrial_mix
# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
 ],
    
    5:  #sub_model
        [
#       ("urbansim.gridcell.is_outside_urban_growth_boundary","OUT_UGB"),    
       ("urbansim.gridcell.is_near_arterial","ART"), #variable name, coefficient name
       ("urbansim.gridcell.is_near_highway","HWY"),  #
#      ("urbansim.gridcell.ln_distance_to_highway","LDHWY"),
#        ("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
        #("urbansim.gridcell.is_in_wetland","WTLND"),#
#        ("urbansim.gridcell.is_in_floodplain","FLOOD"),#
        #("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#
        ('urbansim.gridcell.ln_total_land_value', 'LTLV'),         
        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
        ("ln(urbansim.gridcell.average_income_within_walking_distance)","LINCW"),
#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LPOPW"),
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#         ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#         ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
         ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#         ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
         ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
     #    ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'LE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'LE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'LE_SEW'),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#         ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
          ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
          ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#          ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDEV"),
#         ("urbansim.gridcell.n_recent_development_projects", "NRDP"),
          ("urbansim.gridcell.sum_n_recent_development_projects_within_walking_distance", "NRDPW"),
#         ("urbansim.gridcell.n_residential_units_recently_added_within_walking_distance", "RDUW"),
#         ("urbansim.gridcell.n_commercial_sqft_recently_added_within_walking_distance", "RCSFW"),
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
  #      ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
  #      ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#?        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
  #      ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  

  #        ("urbansim.gridcell.is_plan_type_6","PT_6"),   #industrial
#         ("urbansim.gridcell.is_plan_type_7","PT_7"),    #industrial_mix
# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
 ]
    }

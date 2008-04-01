
import sys
import os
print os.path.join(sys.path[0], r'..\..\..\Estimation\Library')
sys.path.append(os.path.join(sys.path[0], r'..\..\..\Estimation\Library'))
import mdbi

myDB = mdbi.DbConnection(db = 'PSRC_2000_estimation_petecaba',
                        hostname = 'trondheim.cs.washington.edu',
                        username = 'urbansim',
                        password = 'UrbAnsIm4Us')


def GetVariables():
    _vars =[['basic_sector_employment_within_walking_distance','BE_BW'],
            ['building_age','BAGE_BL'],
            ['commercial_sqft_recently_added_within_walking_distance','BSFCWRT'],
            ['constant','BONE'],
            ['gridcell_is_inside_tribal_land','BG_IS_I'],
            ['is_developed','BDVLPD'],
            ['is_in_floodplain','BFLOOD'],
            ['is_in_stream_buffer','BSTRBUF'],
            ['is_in_wetland','BWTLND'],
            ['is_near_arterial','BART'],
            ['is_near_highway','BHWY'],
            ['is_outside_urban_growth_boundary','BO_UGB'],
            ['ln_average_land_value_per_acre_within_walking_distance','BLALVAW'],
            ['ln_average_total_value_per_residential_unit_within_walking_distance','BLAVURW'],
            ['ln_commercial_sqft_recently_added_within_walking_distance','BLSFCWR'],
            ['ln_distance_to_highway','BLD_HY'],
            ['ln_home_access_to_employment_1','BLHAE1'],
            ['ln_industrial_sqft_within_walking_distance','BLSFIW'],
            ['ln_land_value','BLLV'],
            ['ln_percent_commercial_within_walking_distance','BLP_W03'],
            ['ln_percent_governmental_within_walking_distance','BLP_W02'],
            ['ln_percent_industrial_within_walking_distance','BLP_W01'],
            ['ln_percent_mixed_use_within_walking_distance','BLP_W04'],
            ['ln_percent_residential_within_walking_distance','BLP_W05'],
            ['ln_residential_improvement_value_per_residential_unit','BLIVU'],
            ['ln_residential_units','BLDU'],
            ['ln_residential_units_within_walking_distance','BLDUW'],
            ['ln_retail_within_walking_distance','BLSFREW'],
            ['ln_total_employment_within_walking_distance','BLE_W'],
            ['ln_total_improvement_value','BLIV'],
            ['ln_total_land_value_per_acre_within_walking_distance','BLLVA_W'],
            ['ln_total_nonresidential_sqft_within_walking_distance','BLNRSFW'],
            ['ln_total_residential_value_per_residential_unit_within_walking_distance','BLVU_RW'],
            ['ln_total_value','BLV'],
            ['n_recent_transitions_to_commercial_within_walking_distance','BTR03WR'],
            ['n_recent_transitions_to_developed_within_walking_distance','BTRDWRT'],
            ['n_recent_transitions_to_industrial_within_walking_distance','BTR01WR'],
            ['n_recent_transitions_to_residential_within_walking_distance','BTR05WR'],
            ['n_recent_transitions_to_same_type_within_walking_distance','BTRSWRT'],
            ['n_residential_units_recently_added_within_walking_distance','BDURWRT'],
            ['percent_commercial_within_walking_distance','BP03W'],
            ['percent_developed_within_walking_distance','BP_DEV'],
            ['percent_floodplain','BPFL'],
            ['percent_high_income_households_within_walking_distance','BPHIW'],
            ['percent_industrial_within_walking_distance','BP01W'],
            ['percent_low_income_households_within_walking_distance','BPLIW'],
            ['percent_mid_income_households_within_walking_distance','BPMIW'],
            ['percent_minority_households_within_walking_distance','BPMNW'],
            ['percent_open_space','BPOPEN'],
            ['percent_public_space','BPPUB'],
            ['percent_residential_within_walking_distance','BP05W'],
            ['percent_roads','BPROAD'],
            ['percent_same_type_cells_within_walking_distance','BPSTCW'],
            ['percent_slope','BPSLOPE'],
            ['percent_stream_buffer','BPSTBUF'],
            ['percent_water','BPWATER'],
            ['percent_wetland','BPWETLA'],
            ['plantype_1','BPT0001'],
            ['plantype_10','BPT0010'],
            ['plantype_11','BPT0011'],
            ['plantype_2','BPT0002'],
            ['plantype_3','BPT0003'],
            ['plantype_4','BPT0004'],
            ['plantype_5','BPT0005'],
            ['plantype_6','BPT0006'],
            ['plantype_7','BPT0007'],
            ['plantype_8','BPT0008'],
            ['plantype_9','BPT0009'],
            ['proximity_to_development','BPRXDEV'],
            ['residential_units_within_walking_distance','BDURW'],
            ['retail_sector_employment_within_walking_distance','BE_REW'],
            ['service_sector_employment_within_walking_distance','BE_SEW'],
            ['travel_time_to_CBD','BTT_CBD']]
            
   
    #Print '\n'.join(_vars)
    
    return _vars
    
    
def GetSubModels(myDB):
    
    _sub_models_rs = myDB.GetResultsFromQuery('select distinct sub_model_id from developer_model_specification')
    
    #Change into simple list
    _sub_models = []
    for rec in _sub_models_rs[1:]:
        _sub_models.append(rec[0])
        
    return _sub_models


##########################################

_sub_models = GetSubModels(myDB)

_variables = GetVariables()
 
print "processing..."

myDB.DoQuery('delete from developer_model_specification')

for _sm in range(1,24):
    for _var in _variables:
        #for _eq in range (1,24):
        _insert_qry = """INSERT INTO developer_model_specification
        (sub_model_id, equation_id, variable_name, coefficient_name)
        VALUES (""" + str(_sm)+ ", " '-2' ", '" + _var[0] + "', '" + _var[1]+ "')"

        print _insert_qry            
        myDB.DoQuery(_insert_qry)
 
print "Variables inserted."



      
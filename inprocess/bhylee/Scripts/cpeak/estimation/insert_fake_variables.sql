################
#
#	This inserts fake variables into the specification and variable_names tables 
#		so that household variables (and, if need be, gridcell variables) 
#		can be used in estimation.  These variables are not currently output
#		by the estimation data writer.
#

INSERT INTO household_location_choice_model_specification(
	variable_name,
	coefficient_name
)
VALUES 
('age_of_head', 'bAGE'),
('cars', 'bCARS'),
('persons', 'bPRSNS'),
('children', 'bCHLDRN'),
('workers', 'bWRKRS'),
('income', 'bINCOME'),
('race_id', 'bRACE'),
('FAZ', 'bfaz'),
('FAZDISTRICT', 'bFAZDIST'),
('accessibility_tt_all_modes', 'bACTTAL'),
('accessibility_tt_sov', 'bACTTSO'),
('accessibility_tt_walk', 'bACCTWK'),
('accessibility_tt_transit_walk', 'bACCTTW'),
('accessibility_tt_transit_auto', 'bACCTTA'),
('hbw_u_all', 'bHBWUAL'),
('hbw_u_sov', 'bHBWUSO'),
('hbw_u_transit_walk', 'bHBWTRW'),
('hbw_u_walk', 'bHBWWLK'),
('lhae0', 'bOLHAE0'),
('pct_jobs_within_20_sov', 'bPJ20SO'),
('pct_jobs_within_20_transit_walk', 'bPJ20TW'),
('pct_jobs_within_20_walk', 'bPJ20WK'),
('hbnw_car', 'bHBNWCA'),
('hbnw_transit', 'bHBNWTR')
;

CREATE INDEX JOB_ID ON employment_location_choice_model_estimation_data (job_id);

INSERT INTO household_location_choice_model_variable_names(
	variable_name,
	short_name
)
VALUES
('age_of_head', 'AGE'),
('cars', 'CARS'),
('persons', 'PRSNS'),
('children', 'CHLDRN'),
('workers', 'WRKRS'),
('income', 'INCOME'),
('race_id', 'RACE'),
('FAZ', 'faz'),
('FAZDISTRICT', 'FAZDIST'),
('accessibility_tt_all_modes', 'ACTTAL'),
('accessibility_tt_sov', 'ACTTSO'),
('accessibility_tt_walk', 'ACCTWK'),
('accessibility_tt_transit_walk', 'ACCTTW'),
('accessibility_tt_transit_auto', 'ACCTTA'),
('hbw_u_all', 'HBWUAL'),
('hbw_u_sov', 'HBWUSO'),
('hbw_u_transit_walk', 'HBWTRW'),
('hbw_u_walk', 'HBWWLK'),
('lhae0', 'OLHAE0'),
('pct_jobs_within_20_sov', 'PJ20SO'),
('pct_jobs_within_20_transit_walk', 'PJ20TW'),
('pct_jobs_within_20_walk', 'PJ20WK'),
('hbnw_car', 'HBNWCA'),
('hbnw_transit', 'HBNWTR')
;

INSERT INTO household_location_choice_model_specification(
	variable_name,
	coefficient_name
)
VALUES ('grid_id', 'bGRID_ID')
;

INSERT INTO household_location_choice_model_variable_names(
	variable_name,
	short_name
)
VALUES
	('grid_id', 'GRID_ID')
;


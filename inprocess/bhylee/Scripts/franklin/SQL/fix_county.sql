update gridcells_2030 set co_id=49 where ci_id=77;

DROP TABLE IF EXISTS county_2030;
CREATE TABLE county_2030 (co_id int, co_na text);
     
ALTER TABLE county_2030
  ADD COLUMN dur_a int, ADD COLUMN iv_r_a double, 
  ADD COLUMN sf_c_a double, ADD COLUMN iv_c_a double, ADD COLUMN sf_i_a double, ADD COLUMN iv_i_a double, ADD COLUMN sf_g_a double, 
  ADD COLUMN iv_g_a double, ADD COLUMN lv_r_a double, ADD COLUMN lv_nr_a double, ADD COLUMN sf_tot_a double, ADD COLUMN lv_tot_a double, 
  ADD COLUMN js_hb_a double, ADD COLUMN js_nhb_a double, ADD COLUMN js_tot_a double,
  ADD COLUMN hhs_a double, ADD COLUMN pop_a double, ADD COLUMN wrkrs_a double, ADD COLUMN totinc_a double, ADD COLUMN child_a double, 
  ADD COLUMN ageh_a double, ADD COLUMN jobs_a double, ADD COLUMN hb_pct_a double, ADD COLUMN j_3p_a double,
  ADD COLUMN vr_r_a double, ADD COLUMN vr_nr_a double, ADD COLUMN hhsz_a double, ADD COLUMN hhin_a double,
  
  ADD COLUMN dur_z int, ADD COLUMN iv_r_z double,
  ADD COLUMN sf_c_z double, ADD COLUMN iv_c_z double, ADD COLUMN sf_i_z double, ADD COLUMN iv_i_z double, ADD COLUMN sf_g_z double, 
  ADD COLUMN iv_g_z double, ADD COLUMN lv_r_z double, ADD COLUMN lv_nr_z double, ADD COLUMN sf_tot_z double, ADD COLUMN lv_tot_z double, 
  ADD COLUMN js_hb_z double, ADD COLUMN js_nhb_z double, ADD COLUMN js_tot_z double,
  ADD COLUMN hhs_z double, ADD COLUMN pop_z double, ADD COLUMN wrkrs_z double, ADD COLUMN totinc_z double, ADD COLUMN child_z double, 
  ADD COLUMN ageh_z double, ADD COLUMN jobs_z double, ADD COLUMN hb_pct_z double, ADD COLUMN j_3p_z double,
  ADD COLUMN vr_r_z double, ADD COLUMN vr_nr_z double, ADD COLUMN hhsz_z double, ADD COLUMN hhin_z double,

  ADD COLUMN dur_d int, ADD COLUMN iv_r_d double, 
  ADD COLUMN sf_c_d double, ADD COLUMN iv_c_d double, ADD COLUMN sf_i_d double, ADD COLUMN iv_i_d double, ADD COLUMN sf_g_d double, 
  ADD COLUMN iv_g_d double, ADD COLUMN lv_r_d double, ADD COLUMN lv_nr_d double, ADD COLUMN sf_tot_d double, ADD COLUMN lv_tot_d double, 
  ADD COLUMN js_hb_d double, ADD COLUMN js_nhb_d double, ADD COLUMN js_tot_d double,
  ADD COLUMN hhs_d double, ADD COLUMN pop_d double, ADD COLUMN wrkrs_d double, ADD COLUMN totinc_d double, ADD COLUMN child_d double, 
  ADD COLUMN ageh_d double, ADD COLUMN jobs_d double, ADD COLUMN hb_pct_d double, ADD COLUMN j_3p_d double,
  ADD COLUMN vr_r_d double, ADD COLUMN vr_nr_d double, ADD COLUMN hhsz_d double, ADD COLUMN hhin_d double;

CREATE INDEX county_2030_co_id
     ON county_2030 (co_id);
   
INSERT INTO county_2030
SELECT co_id AS co_id,
    NULL AS co_na,
    SUM(dur_a) AS dur_a, 
    SUM(iv_r_a) AS iv_r_a, 
    SUM(sf_c_a) AS sf_c_a, 
    SUM(iv_c_a) AS iv_c_a, 
    SUM(sf_i_a) AS sf_i_a,
    SUM(iv_i_a) AS iv_i_a, 
    SUM(sf_g_a) AS sf_g_a, 
    SUM(iv_g_a) AS iv_g_a, 
    SUM(lv_r_a) AS lv_r_a, 
    SUM(lv_nr_a) AS lv_nr_a, 
    SUM(sf_tot_a) AS sf_tot_a, 
    SUM(lv_tot_a) AS lv_tot_a, 
    SUM(js_hb_a) AS js_hb_a, 
    SUM(js_nhb_a) AS js_nhb_a, 
    SUM(js_tot_a) AS js_tot_a, 
    SUM(hhs_a) AS hhs_a, 
    SUM(pop_a) AS pop_a, 
    SUM(wrkrs_a) AS wrkrs_a, 
    SUM(totinc_a) AS totinc_a, 
    SUM(child_a) AS child_a, 
    AVG(ageh_a) AS ageh_a, 
    SUM(jobs_a) AS jobs_a, 
    AVG(hb_pct_a) AS hb_pct_a, 
    SUM(j_3p_a) AS j_3p_a,
    NULL AS vr_r_a, 
    NULL AS vr_nr_a,
    NULL AS hhsz_a,
    NULL AS hhin_a,

    SUM(dur_z) AS dur_z, 
    SUM(iv_r_z) AS iv_r_z, 
    SUM(sf_c_z) AS sf_c_z, 
    SUM(iv_c_z) AS iv_c_z, 
    SUM(sf_i_z) AS sf_i_z,
    SUM(iv_i_z) AS iv_i_z, 
    SUM(sf_g_z) AS sf_g_z, 
    SUM(iv_g_z) AS iv_g_z, 
    SUM(lv_r_z) AS lv_r_z, 
    SUM(lv_nr_z) AS lv_nr_z, 
    SUM(sf_tot_z) AS sf_tot_z, 
    SUM(lv_tot_z) AS lv_tot_z, 
    SUM(js_hb_z) AS js_hb_z, 
    SUM(js_nhb_z) AS js_nhb_z, 
    SUM(js_tot_z) AS js_tot_z, 
    SUM(hhs_z) AS hhs_z, 
    SUM(pop_z) AS pop_z, 
    SUM(wrkrs_z) AS wrkrs_z, 
    SUM(totinc_z) AS totinc_z, 
    SUM(child_z) AS child_z, 
    AVG(ageh_z) AS ageh_z, 
    SUM(jobs_z) AS jobs_z, 
    AVG(hb_pct_z) AS hb_pct_z,  
    SUM(j_3p_z) AS j_3p_z,
    NULL AS vr_r_z, 
    NULL AS vr_nr_z, 
    NULL AS hhsz_z,
    NULL AS hhin_z,
    
    SUM(dur_d) AS dur_d, 
    SUM(iv_r_d) AS iv_r_d, 
    SUM(sf_c_d) AS sf_c_d, 
    SUM(iv_c_d) AS iv_c_d, 
    SUM(sf_i_d) AS sf_i_d,
    SUM(iv_i_d) AS iv_i_d, 
    SUM(sf_g_d) AS sf_g_d, 
    SUM(iv_g_d) AS iv_g_d, 
    SUM(lv_r_d) AS lv_r_d, 
    SUM(lv_nr_d) AS lv_nr_d, 
    SUM(sf_tot_d) AS sf_tot_d, 
    SUM(lv_tot_d) AS lv_tot_d, 
    SUM(js_hb_d) AS js_hb_d, 
    SUM(js_nhb_d) AS js_nhb_d, 
    SUM(js_tot_d) AS js_tot_d, 
    SUM(hhs_d) AS hhs_d, 
    SUM(pop_d) AS pop_d, 
    SUM(wrkrs_d) AS wrkrs_d, 
    SUM(totinc_d) AS totinc_d, 
    SUM(child_d) AS child_d, 
    NULL AS ageh_d, 
    SUM(jobs_d) AS jobs_d, 
    NULL AS hb_pct_d,  
    SUM(j_3p_d) AS j_3p_d,
    NULL AS vr_r_d, 
    NULL AS vr_nr_d,
    NULL AS hhsz_d,
    NULL AS hhin_d
FROM gridcells_2030
GROUP BY co_id;

update county_2030
     set vr_r_a = 1 - (hhs_a/dur_a),
          vr_nr_a = 1 - (jobs_a/js_tot_a),
          vr_r_z = 1 - (hhs_z/dur_z),
          vr_nr_z = 1 - (jobs_z/js_tot_z),
          vr_r_d = (hhs_a/dur_a) - (hhs_z/dur_z),
          vr_nr_d = (jobs_a/js_tot_a) - (jobs_z/js_tot_z),
          ageh_d = ageh_z - ageh_d,
          hb_pct_d = hb_pct_z - hb_pct_a,
          hhsz_a = pop_a/hhs_a,
          hhsz_z = pop_z/hhs_z,
          hhsz_d = (pop_z/hhs_z) - (pop_a/hhs_a),
          hhin_a = totinc_a/hhs_a,
          hhin_z = totinc_z/hhs_z,
          hhin_d = (totinc_z/hhs_z) - (totinc_a/hhs_a);

update county_2030 AS a, WFRC_1997_baseyear.counties AS b
     set a.co_na = b.county_name
     where a.co_id = b.county_id;

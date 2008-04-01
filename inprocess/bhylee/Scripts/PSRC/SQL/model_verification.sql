use PSRC_2000_output_franklin_non_hb_verification;

# if not already done...
create index verification_data_for_sector_13_job_id_grid_id on verification_data_for_sector_13 (job_id, grid_id);

# Summarize verification tables

describe verification_data_for_sector_13;

# Get sample rows

select
     job_id,
     grid_id,
     utility,
     cum_prob,
     rand_num,
     chosen
from verification_data_for_sector_13
limit 10;

select
     e_bw_var,       # sectors: 1,2,3,4,5,6,7,8,9,10,11,13
     e_bw_coeff,     # sectors: 1,2,3,4,5,6,7,8,9,10,11,13
     age_bl_var,     # sectors: 8,12,13
     age_bl_coeff,   # sectors: 8,12,13
     art_var,        # sectors: 1,3,4,5,6,7,8,9,10,11,12,13
     art_coeff,      # sectors: 1,3,4,5,6,7,8,9,10,11,12,13
     hwy_var,        # sectors: 1,2,3,4,5,10,11,13
     hwy_coeff,      # sectors: 1,2,3,4,5,10,11,13
     lalvaw_var,     # sectors: 3,4,7,9,11,13
     lalvaw_coeff,   # sectors: 3,4,7,9,11,13
     lsfc_var,       # sectors: 1,5,6,7,8,9,10,12,13
     lsfc_coeff,     # sectors: 1,5,6,7,8,9,10,12,13
#     livu_var,       # sectors: 9
#     livu_coeff,     # sectors: 9
     livuw_var,      # sectors: 7,13
     livuw_coeff,    # sectors: 7,13
     lsfiw_var,      # sectors: 4,5,6,7,8,12,13
     lsfiw_coeff,    # sectors: 4,5,6,7,8,12,13
     ldu_var,        # sectors: 1,2,3,5,6,8,11,12,13
     ldu_coeff,      # sectors: 1,2,3,5,6,8,11,12,13
#     lduw_var,       # sectors: 4,7
#     lduw_coeff,     # sectors: 4,7
#     lnrsfw_var,     # sectors: 5,6,9,11
#     lnrsfw_coeff,   # sectors: 5,6,9,11
#     lv_var,         # sectors: 1,2,5,6,8,9,10,11,12
#     lv_coeff,       # sectors: 1,2,5,6,8,9,10,11,12
#     lwap_1_var,     # sectors: 1,2,6,7,9,12
#     lwap_1_coeff,   # sectors: 1,2,6,7,9,12
#     lwae_1_var,     # sectors: 1,2,3,5,10,11
#     lwae_1_coeff,   # sectors: 1,2,3,5,10,11
#     phiw_var,       # sectors: 10
#     phiw_coeff,     # sectors: 10
#     pliw_var,       # sectors: 1,2,4,5,6,7,10,11
#     pliw_coeff,     # sectors: 1,2,4,5,6,7,10,11
     pmiw_var,       # sectors: 1,2,6,8,9,12,13
     pmiw_coeff,     # sectors: 1,2,6,8,9,12,13
     e_rew_var,      # sectors: 1,2,3,4,6,7,8,10,11,13
     e_rew_coeff,    # sectors: 1,2,3,4,6,7,8,10,11,13
     e_saw_var,      # sectors: 1,2,3,4,5,6,7,8,9,10,11,12,13
     e_saw_coeff,    # sectors: 1,2,3,4,5,6,7,8,9,10,11,12,13
     e_sew_var,      # sectors: 1,2,3,5,7,8,10,11,12,13
     e_sew_coeff,    # sectors: 1,2,3,5,7,8,10,11,12,13
     tt_cbd_var,     # sectors: 3,4,5,6,8,9,10,11,12,13
     tt_cbd_coeff    # sectors: 3,4,5,6,8,9,10,11,12,13
from verification_data_for_sector_13
limit 10;

# Get mins, maxs

select 
     min(utility), 
     max(utility), 
     min(cum_prob), # should be positive, but close to 0
     max(cum_prob), # should be 1
     min(rand_num), # should be close to 0
     max(rand_num), # should be close to, but smaller than, 1
     min(chosen), # should be 0
     max(chosen), # should be 1
     # In the following, for each "*_coeff", the min and max should be the same.
     min(e_bw_var), 
     max(e_bw_var), 
     min(e_bw_coeff),
     max(e_bw_coeff),
     min(age_bl_var), 
     max(age_bl_var), 
     min(age_bl_coeff),
     max(age_bl_coeff),
     min(art_var),
     max(art_var),
     min(art_coeff),
     max(art_coeff),
     min(hwy_var),
     max(hwy_var),
     min(hwy_coeff),
     max(hwy_coeff),
     min(lalvaw_var),
     max(lalvaw_var),
     min(lalvaw_coeff),
     max(lalvaw_coeff),
     min(lsfc_var),
     max(lsfc_var),
     min(lsfc_coeff),
     max(lsfc_coeff),
#     min(livu_var),
#     max(livu_var),
#     min(livu_coeff),
#     max(livu_coeff),
     min(livuw_var),
     max(livuw_var),
     min(livuw_coeff),
     max(livuw_coeff),
     min(lsfiw_var),
     max(lsfiw_var),
     min(lsfiw_coeff),
     max(lsfiw_coeff),
     min(ldu_var),
     max(ldu_var),
     min(ldu_coeff),
     max(ldu_coeff),
#     min(lduw_var),
#     max(lduw_var),
#     min(lduw_coeff),
#     max(lduw_coeff),
#     min(lnrsfw_var),
#     max(lnrsfw_var),
#     min(lnrsfw_coeff),
#     max(lnrsfw_coeff),
#     min(lv_var),
#     max(lv_var),
#     min(lv_coeff),
#     max(lv_coeff),
#     min(lwap_1_var),
#     max(lwap_1_var),
#     min(lwap_1_coeff),
#     max(lwap_1_coeff),
#     min(lwae_1_var),
#     max(lwae_1_var),
#     min(lwae_1_coeff),
#     max(lwae_1_coeff),
#     min(phiw_var),
#     max(phiw_var),
#     min(phiw_coeff),
#     max(phiw_coeff),
#     min(pliw_var),
#     max(pliw_var),
#     min(pliw_coeff),
#     max(pliw_coeff),
     min(pmiw_var),
     max(pmiw_var),
     min(pmiw_coeff),
     max(pmiw_coeff),
     min(e_rew_var),
     max(e_rew_var),
     min(e_rew_coeff),
     max(e_rew_coeff),
     min(e_saw_var),
     max(e_saw_var),
     min(e_saw_coeff),
     max(e_saw_coeff),
     min(e_sew_var),
     max(e_sew_var),
     min(e_sew_coeff),
     max(e_sew_coeff),
     min(tt_cbd_var),
     max(tt_cbd_var),
     min(tt_cbd_coeff),
     max(tt_cbd_coeff)
from verification_data_for_sector_13 \G

# Make room for check columns

alter table verification_data_for_sector_13 
     add column (
          utility_check double,
          exp_utility_check double,
          ind_prob_check double,
          cum_prob_check double,
          chosen_check integer);

# Compute utility check
#    do utility calc

update verification_data_for_sector_13
     set utility_check = 0
          + e_bw_var*e_bw_coeff
          + age_bl_var*age_bl_coeff
          + art_var*art_coeff
          + hwy_var*hwy_coeff
          + lalvaw_var*lalvaw_coeff
          + lsfc_var*lsfc_coeff
#          + livu_var*livu_coeff
          + livuw_var*livuw_coeff
          + lsfiw_var*lsfiw_coeff
          + ldu_var*ldu_coeff
#          + lduw_var*lduw_coeff
#          + lnrsfw_var*lnrsfw_coeff
#          + lv_var*lv_coeff
#          + lwap_1_var*lwap_1_coeff
#          + lwae_1_var*lwae_1_coeff
#          + phiw_var*phiw_coeff
#          + pliw_var*pliw_coeff
          + pmiw_var*pmiw_coeff
          + e_rew_var*e_rew_coeff
          + e_saw_var*e_saw_coeff
          + e_sew_var*e_sew_coeff
          + tt_cbd_var*tt_cbd_coeff;

#    compare utility check with reported utility

select job_id, grid_id, utility, utility_check from verification_data_for_sector_13 where round(utility,5)<>round(utility_check,5) and utility>-1.7e+308;

# Compute probability
#    compute exponented utility for each job/grid

update verification_data_for_sector_13
     set exp_utility_check=exp(utility);

#    compute sums of exponented utility for each job
drop table if exists sector_13_job_composites;
create table sector_13_job_composites
     select job_id as job_id,
          sum(exp_utility_check) as sum_exp_utility_check
     from verification_data_for_sector_13
     group by job_id;
create index sector_13_job_composites_job_id on sector_13_job_composites (job_id);

#    bring sums from each job into each job/grid to compute individual probabilities
update verification_data_for_sector_13 as a, sector_13_job_composites as b
     set a.ind_prob_check=a.exp_utility_check/b.sum_exp_utility_check
     where a.job_id=b.job_id;

# Compute chosen grid cells

#    look for improperly chosen gridcells

select job_id, 
     grid_id, 
     ind_prob_check as ind_prob,
     cum_prob,
     rand_num,
     chosen
from verification_data_for_sector_13
     where chosen=1
          and (rand_num>cum_prob or rand_num<cum_prob-ind_prob_check);

#    look for improperly unchosen gridcells
select job_id, 
     grid_id, 
     ind_prob_check as ind_prob,
     cum_prob,
     rand_num,
     chosen
from verification_data_for_sector_13
     where chosen=0
          and (rand_num<=cum_prob and rand_num>=cum_prob-ind_prob_check);

#    check counts of chosen gridcells

drop table if exists sector_13_chosen_gridcells;
create table sector_13_chosen_gridcells
     select job_id,
          count(grid_id) as chosen_cells
     from verification_data_for_sector_13
     where chosen=1
     group by job_id;

select * from sector_13_chosen_gridcells where chosen_cells<>1;

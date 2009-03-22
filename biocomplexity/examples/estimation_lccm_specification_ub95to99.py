# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

specification = {}

specification = {
2:
    {
    "equation_ids":(1,2),
    "constant":(0, "act_2_2"),
    "c750":("c750_2_1", 0),
    "di":("di_2_1", 0),
    "dloc":("dloc_2_1", 0),
    "dos":("dos_2_1", 0),
    "dtim":("dtim_2_1", 0),
    "hai":("hai_2_1", 0),
    "hd1":("hd1_2_1", 0),
    "hmps":("hmps_2_1", 0),
 #   "pcd":("pcd_2_1", 0),   - jeff removed pcd from all on 21 Feb 2006
    "pfld":("pfld_2_1", 0),
    "pgr":("pgr_2_1", 0),
    "phu":("phu_2_1", 0),
    "plu":("plu_2_1", 0),
    "shei":("shei_2_1", 0),
    },
 3:
    {
        "equation_ids":(1,2,3),
    "constant":(0,"act_3_2","act_3_3"),
    "amps":(0,"amps_3_2", 0),
    "c750":("c750_3_1",0, 0),
    "dag":(0,"dag_3_2", 0),
    "de":(0,"de_3_2", 0),
    "dpub":("dpub_3_1","dpub_3_2", 0),
    "dtim":("dtim_3_1",0, 0),
    "gai":(0,"gai_3_2", 0),
    "gmps":("gmps_3_1",0, 0),
    "hai":("hai_3_1","hai_3_2", 0),
    "hd1":("hd1_3_1",0, 0),
 #   "pcd":("pcd_3_1","pcd_3_2", 0),
    "pcf":(0,"pcf_3_2", 0),
    "pfld":("pfld_3_1","pfld_3_2", 0),
    "pgr":("pgr_3_1",0, 0),
    "phu":("phu_3_1","phu_3_2", 0),
    "plu":("plu_3_1",0, 0),
    "pmf":(0,"pmf_3_2", 0),
    "pmu":("pmu_3_1","pmu_3_2", 0),
    "pslp":("pslp_3_1",0, 0),
    "pwa":("pwa_3_1",0, 0),
    "shei":("shei_3_1","shei_3_2", 0),
    "ugl":(0,"ugl_3_2", 0)
    },
4:
    {
    }, 
5:
    {
            "equation_ids":(1,2,3,5,6),  # note: this is the to_id's
    "constant":("act_5_1","act_5_2","act_5_3","act_5_5",0),
    "aai":(0,0,"aai_5_3", 0,0),
    "c750":("c750_5_1",0,0, 0,0),
    "crit":("crit_5_1",0,0, 0,0),
    "dag":(0,"dag_5_2",0, 0,0),
    "dcri":("dcri_5_1","dcri_5_2",0, 0,0),
    "dloc":("dloc_5_1",0,0, 0,0),
    "dmu":(0,"dmu_5_2",0, 0,0),
    "dnlr":("dnlr_5_1",0,0, 0,0),
    "dres":(0,"dres_5_2",0, 0,0),
    "dtim":(0,"dtim_5_2",0, 0,"dtim_5_6"),
    "dwat":("dwat_5_1","dwat_5_2",0, 0,0),
    "dwet":(0,0,"dwet_5_3", 0,0),
    "gai":("gai_5_1",0,0, 0,"gai_5_6"),
    "gmps":(0,0,"gmps_5_3", 0,0),
    "h450":("h450_5_1",0,0, 0,0),
    "h750":("h750_5_1",0,0, 0,0),
    "hai":("hai_5_1","hai_5_2",0, 0,0),
    "hd1":("hd1_5_1",0,0, 0,0),
#    "pcd":("pcd_5_1","pcd_5_2","pcd_5_3", 0,0),
    "pcf":(0,0,0, 0,"pcf_5_6"),
    "pfld":(0,"pfld_5_2",0, 0,0),
    "pgr":(0,"pgr_5_2","pgr_5_3", 0,0),
    "phu":("phu_5_1","phu_5_2",0, 0,0),
    "plu":("plu_5_1",0,"plu_5_3", 0,0),
    "pmf":(0,"pmf_5_2",0, 0,"pmf_5_6"),
    "pmu":("pmu_5_1","pmu_5_2","pmu_5_3", 0,0),
    "psg":("psg_5_1",0,0, 0,0),
    "pslp":("pslp_5_1",0,0, 0,0),
    "pstr":("pstr_5_1","pstr_5_2",0, 0,0),
    "pub":("pub_5_1",0,0, 0,0),
    "shei":("shei_5_1",0,0, 0,0),
    "ugl":(0,0,"ugl_5_3", 0,0)
    }, 
6:
    {
            "equation_ids":(1,2,3,5,6),  # note: this is the to_id's
    "constant":("act_6_","act_6_2","act_6_3",0,"act_6_6"),
    "aai":(0,0,"aai_6_3",0, 0),
    "c450":("c450_6_1",0,0,0, 0),
    "c750":(0,"c750_6_2",0,0, 0),
    "dc":("dc_6_1",0,0,0, 0),
    "dcri":("dcri_6_1",0,0,0, 0),
    "de":("de_6_1",0,0,0, 0),
    "dfre":("dfre_6_1",0,0,0, 0),
    "di":("di_6_1",0,0,0, 0),
    "dloc":("dloc_6_1","dloc_6_2","dloc_6_3",0, 0),
    "dmu":("dmu_6_1",0,0,0, 0),
    "dnlr":(0,0,"dnlr_6_3",0, 0),
    "dos":("dos_6_1","dos_6_2",0,0, 0),
    "dprd":("dprd_6_1",0,0,0, 0),
    "dres":("dres_6_1",0,0,0, 0),
    "dtim":(0,"dtim_6_2","dtim_6_3",0, 0,),
    "gai":(0,"gai_6_2","gai_6_3","gai_6_5", 0),
 #   "pcd":("pcd_6_1","pcd_6_2","pcd_6_3",0, 0),
    "pcri":(0,"pcri_6_2",0,0, 0),
    "pes":(0,0,"pes_6_3",0, 0),
    "pgr":("pgr_6_1","pgr_6_2","pgr_6_3","pgr_6_5", 0),
    "phu":("phu_6_1",0,0,0, 0),
    "plu":("plu_6_1","plu_6_2","plu_6_3",0, 0),
    "pmf":(0,"pmf_6_2",0,0, 0),
    "pmu":("pmu_6_1","pmu_6_2","pmu_6_3","pmu_6_5", 0),
    "pslp":("pslp_6_1","pslp_6_2","pslp_6_3",0, 0),
    "pstr":("pstr_6_1",0,0,0, 0),
    "pub":(0,"pub_6_2","pub_6_3",0, 0),
    "pwa":(0,0,"pwa_6_3",0, 0),
    "pwet":("pwet_6_1","pwet_6_2",0,0, 0),
    "shei":(0,0,0,"shei_6_5", 0),
    "tiv":(0,"tiv_6_2",0,0, 0),
    "ugl":(0,0,"ugl_6_3","ugl_6_5", 0),
    }, 
7:
   {
         "equation_ids":(3,7),
    "constant":(0, "act_7_7"),
    "aai":("aai_7_3", 0),
    "blmz":("blmz_7_3", 0),
    "dloc":("dloc_7_3", 0),
    "dpub":("dpub_7_3", 0),
    "pag":("pag_7_3", 0),
#    "pcd":("pcd_7_3", 0),
    "pgr":("pgr_7_3", 0),
    "pmf":("pmf_7_3", 0),
    "psg":("psg_7_3", 0),
    "tiv":("tiv_7_3", 0),
    "ugl":("ugl_7_3", 0),
    }, 
10:
   {
     "equation_ids":(3,5,10),
    "constant":(0,"act_10_5","act_10_10"),
    "aai":("aai_10_3",0, 0),
    "blmz":("blmz_10_3",0, 0),
    "dag":(0,"dag_10_5", 0),
    "dloc":("dloc_10_3",0, 0),
    "dnlr":(0,"dnlr_10_5", 0),
    "dpub":("dpub_10_3","dpub_10_5", 0),
    "dtim":(0,"dtim_10_5", 0),
    "dwat":(0,"dwat_10_5", 0),
    "gmps":(0,"gmps_10_5", 0),
    "h450":("h450_10_3",0, 0),
    "h750":("h750_10_3",0, 0),
#    "pcd":("pcd_10_3",0, 0),
    "pcf":(0,"pcf_10_5", 0),
    "pfld":(0,"pfld_10_5", 0),
    "pgr":("pgr_10_3","pgr_10_5", 0),
    "plu":("plu_10_3",0, 0),
    "pmf":("pmf_10_3",0, 0),
    "psg":("psg_10_3","psg_10_5", 0),
    "pub":("pub_10_3","pub_10_5", 0),
    "pwa":("pwa_10_3",0, 0),
    "ugl":("ugl_10_3","ugl_10_5", 0),
     },  
8:
     {
    "equation_ids": (9,),   # note the comma after "9"
    "constant":("act_8_9",),
    },  
11:
    {
    "equation_ids": (11,),   # note the comma after "9"
    "constant":("act_11_11",),
    },  
12:
     {
    "equation_ids": (12,),   # note the comma after "9"
    "constant":("act_12_12",),    
     },
13:
     {
    "equation_ids": (13,),   # note the comma after "9"
    "constant":("act_13_13",),
    },  
14:
     {
    "equation_ids": (14,),   # note the comma after "9"
    "constant":("act_14_14",),
      }
 }
    
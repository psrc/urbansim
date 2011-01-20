# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

specification = {}

specification = {
2:
    {
    "equation_ids":(1,2),
    "constant":(0, "act_2_2"),
    "amps":("amps_2_1", 0),
    "c750":("c750_2_1", 0),
    "cd1":("cd1_2_1", 0),
    "de":("de_2_1", 0),
    "dfre":("dfre_2_1", 0),
    "dres":("dres_2_1", 0),
    "h450":("h450_2_1", 0),
    "hai":("hai_2_1", 0),
    "hd1":("hd1_2_1", 0),
    "pgr":("pgr_2_1", 0),
    "plu":("plu_2_1", 0),
   "shei":("shei_2_1", 0),
    "ugl":("ugl_2_1", 0)
    },
 3:
    {
    "equation_ids":(2,3),
    "constant":(0, "act_3_3"),
    "amps":("amps_3_2", 0),
    "blmz":("blmz_3_2", 0),
    "c750":("c750_3_2", 0),
    "dcbd":("dcbd_3_2", 0),
    "dloc":("dloc_3_2", 0),
    "dnlr":("dnlr_3_2", 0),
    "hmps":("hmps_3_2", 0),
    "pcri":("pcri_3_2", 0),
    "pfld":("pfld_3_2", 0),
    "pmu":("pmu_3_2", 0),
    "psg":("psg_3_2", 0),
    "pwet":("pwet_3_2", 0),
    "ugl":("ugl_3_2", 0)
    },
4:
    {
    }, 
5:
    {
    "equation_ids":(2,3,5,6,7),  # note: this is the to_id's
    "constant":("act_5_2","act_5_3","act_5_5",0,"act_5_7"),
    "aai":(0,0,0,"aai_5_6","aai_5_7"),
    "amps":("amps_5_2",0,0,0,0),
    "blmz":(0,"blmz_5_3",0,"blmz_5_6",0),
    "cd1":("cd1_5_2",0,0,"cd1_5_6",0),
    "dag":(0,0,0,"dag_5_6","dag_5_7"),
    "dcbd":(0,0,0,0,"dcbd_5_7"),
    "dcri":(0,0,0,"dcri_5_6","dcri_5_7"),
    "dloc":("dloc_5_2","dloc_5_3",0,0,0),
    "dnlr":(0,"dnlr_5_3",0,0,0),
    "dos":(0,0,0,"dos_5_6",0),
    "dprd":("dprd_5_2",0,0,0,0),
    "dtim":(0,0,0,"dtim_5_6",0),
    "dwat":("dwat_5_2",0,0,0,0),
    "dwet":(0,0,0,0,"dwet_5_7"),
    "gmps":(0,0,0,"gmps_5_6","gmps_5_7"),
    "h750":(0,0,0,0,"h750_5_7"),
    "hd1":(0,"hd1_5_3",0,0,0),
    "mai":(0,0,0,0,"mai_5_7"),
    "pcc":(0,0,0,0,"pcc_5_7"),
    "pcri":(0,0,0,"pcri_5_6","pcri_5_7"),
    "plu":("plu_5_2","plu_5_3",0,"plu_5_6","plu_5_7"),
    "pmu":("pmu_5_2",0,0,"pmu_5_6","pmu_5_7"),
    "psg":(0,0,0,0,"psg_5_7"),
    "pstr":("pstr_5_2",0,0,"pstr_5_6",0),
    "shei":("shei_5_2",0,0,0,"shei_5_7"),
    "sslp":(0,"sslp_5_3",0,0,0),
    "tiv":(0,0,0,0,"tiv_5_7"),
    "ugl":("ugl_5_2",0,0,0,0)
    }, 
6:
    {
    "equation_ids":(2,3,5,6,8),  # note: this is the to_id's
    "constant":("act_6_2","act_6_3",0,"act_6_6","act_6_8"),
    "aai":("aai_6_2","aai_6_3",0,0,"aai_6_8"),
    "amps":(0,0,0,0,"amps_6_8"),
    "blmz":(0,0,0,0,"blmz_6_8"),
    "cd1":("cd1_6_2",0,0,0,0),
    "crit":(0,"crit_6_3",0,0,0),
    "dcbd":(0,0,0,0,"dcbd_6_8"),
    "dcri":("dcri_6_2","dcri_6_3",0,0,0),
    "dloc":("dloc_6_2","dloc_6_3",0,0,0),
    "dnlr":("dnlr_6_2","dnlr_6_3","dnlr_6_5",0,0),
    "dos":(0,"dos_6_3",0,0,0),
    "dprd":(0,0,"dprd_6_5",0,"dprd_6_8"),
    "dpub":("dpub_6_2",0,0,0,0),
    "dtim":("dtim_6_2","dtim_6_3",0,0,"dtim_6_8"),
    "fmps":("fmps_6_2",0,0,0,"fmps_6_8"),
    "mai":(0,0,0,0,"mai_6_8"),
   "pag":("pag_6_2",0,0,0,0),
    "pcc":("pcc_6_2","pcc_6_3",0,0,0),
    "pcf":("pcf_6_2",0,0,0,"pcf_6_8"),
    "pes":("pes_6_2","pes_6_3","pes_6_5",0,"pes_6_8"),
    "pgr":("pgr_6_2",0,"pgr_6_5",0,0),
    "plu":(0,"plu_6_3",0,0,0),
    "psg":(0,"psg_6_3",0,0,0),
    "pslp":("pslp_6_2","pslp_6_3",0,0,0),
    "pstr":("pstr_6_2","pstr_6_3",0,0,"pstr_6_8"),
    "pub":("pub_6_2",0,0,0,0),
    "pwa":(0,0,0,0,"pwa_6_8"),
    "shei":("shei_6_2",0,"shei_6_5",0,"shei_6_8"),
    "tiv":(0,0,0,0,"tiv_6_8"),
    "ugl":("ugl_6_2","ugl_6_3",0,0,0) 
    }, 
7:
   {
    "equation_ids":(2,3,5,7,8),  # note: this is the to_id's
    "constant":("act_7_2","act_7_3","act_7_5","act_7_7",0),
    "aai":("aai_7_2","aai_7_3",0,0,0),
    "amps":(0,0,0,0,"amps_7_8"),
    "blmz":(0,"blmz_7_3",0,0,"blmz_7_8"),
    "dcbd":("dcbd_7_2",0,0,0,0),
    "dloc":("dloc_7_2","dloc_7_3",0,0,0),
    "dnlr":("dnlr_7_2","dnlr_7_3","dnlr_7_5",0,0),
    "dos":(0,"dos_7_3",0,0,"dos_7_8"),
    "dprd":(0,0,0,0,"dprd_7_8"),
    "dpub":(0,0,0,0,"dpub_7_8"),
    "dres":("dres_7_2",0,0,0,0),
    "dtim":("dtim_7_2","dtim_7_3",0,0,0),
    "dwet":("dwet_7_2",0,0,0,0),
    "gai":(0,0,"gai_7_5",0,0),
    "gmps":("gmps_7_2","gmps_7_3",0,0,0),
    "pag":("pag_7_2",0,0,0,0),
    "pcc":(0,"pcc_7_3","pcc_7_5",0,"pcc_7_8"),
    "pfld":("pfld_7_2",0,0,0,0),
    "pgr":("pgr_7_2",0,0,0,0),
    "plu":("plu_7_2","plu_7_3",0,0,0),
    "psg":(0,"psg_7_3","psg_7_5",0,"psg_7_8"),
    "pslp":("pslp_7_2",0,0,0,0),
    "pstr":("pstr_7_2",0,0,0,0),
    "pub":("pub_7_2","pub_7_3","pub_7_5",0,"pub_7_8"),
    "tiv":("tiv_7_2","tiv_7_3",0,0,0),
    "ugl":("ugl_7_2","ugl_7_3",0,0,"ugl_7_8")
    }, 
10:
   {
    "equation_ids":(3,5,6,10),  # note: this is the to_id's
    "constant":("act_10_3","act_10_5",0, "act_10_10"),
    "aai":("aai_10_3",0,0,0),
    "dag":(0,"dag_10_5","dag_10_6",0),
    "dcbd":("dcbd_10_3","dcbd_10_5",0,0),
    "dfre":("dfre_10_3","dfre_10_5","dfre_10_6",0),
    "dloc":(0,"dloc_10_5","dloc_10_6",0),
    "dnlr":("dnlr_10_3","dnlr_10_5","dnlr_10_6",0),
    "dres":("dres_10_3",0,0,0),
    "dtim":(0,"dtim_10_5","dtim_10_6",0),
    "gmps":("gmps_10_3","gmps_10_5","gmps_10_6",0),
    "h750":(0,"h750_10_5",0,0),
    "pag":(0,0,"pag_10_6",0),
    "pcc":(0,"pcc_10_5","pcc_10_6",0),
    "pfld":(0,"pfld_10_5","pfld_10_6",0),
    "plu":("plu_10_3","plu_10_5","plu_10_6",0),
    "pwa":(0,0,"pwa_10_6",0),
    "pwet":("pwet_10_3",0,0,0),
    "shei":(0,"shei_10_5",0,0),
    "sslp":("sslp_10_3",0,0,0),
    "tiv":(0,0,"tiv_10_6",0),
    "ugl":(0,0,"ugl_10_6",0)
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
    
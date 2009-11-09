// household location choice model - Eugene
[Beta]
// Name Value  LowerBound UpperBound  status (0=variable, 1=fixed)
b_dur_nc	0	-1e+06	1e+06	0
b_pmiw_m	0	-1e+06	1e+06	0
b_pmnwmj	0	-1e+06	1e+06	0
b_phiw_h	0	-1e+06	1e+06	0
b_pliw_l	0	-1e+06	1e+06	0

[Choice]
choice

[Utilities]
// Id Name  Avail  linear-in-parameter expression (beta1*x1 + beta2*x2 + ... )
1 alt1 av b_dur_nc * dur_nc_1 + b_pmiw_m * pmiw_m_1 + b_pmnwmj * pmnwmj_1 + b_phiw_h * phiw_h_1 + b_pliw_l * pliw_l_1
2 alt2 av b_dur_nc * dur_nc_2 + b_pmiw_m * pmiw_m_2 + b_pmnwmj * pmnwmj_2 + b_phiw_h * phiw_h_2 + b_pliw_l * pliw_l_2
3 alt3 av b_dur_nc * dur_nc_3 + b_pmiw_m * pmiw_m_3 + b_pmnwmj * pmnwmj_3 + b_phiw_h * phiw_h_3 + b_pliw_l * pliw_l_3
4 alt4 av b_dur_nc * dur_nc_4 + b_pmiw_m * pmiw_m_4 + b_pmnwmj * pmnwmj_4 + b_phiw_h * phiw_h_4 + b_pliw_l * pliw_l_4
5 alt5 av b_dur_nc * dur_nc_5 + b_pmiw_m * pmiw_m_5 + b_pmnwmj * pmnwmj_5 + b_phiw_h * phiw_h_5 + b_pliw_l * pliw_l_5
6 alt6 av b_dur_nc * dur_nc_6 + b_pmiw_m * pmiw_m_6 + b_pmnwmj * pmnwmj_6 + b_phiw_h * phiw_h_6 + b_pliw_l * pliw_l_6
7 alt7 av b_dur_nc * dur_nc_7 + b_pmiw_m * pmiw_m_7 + b_pmnwmj * pmnwmj_7 + b_phiw_h * phiw_h_7 + b_pliw_l * pliw_l_7
8 alt8 av b_dur_nc * dur_nc_8 + b_pmiw_m * pmiw_m_8 + b_pmnwmj * pmnwmj_8 + b_phiw_h * phiw_h_8 + b_pliw_l * pliw_l_8
9 alt9 av b_dur_nc * dur_nc_9 + b_pmiw_m * pmiw_m_9 + b_pmnwmj * pmnwmj_9 + b_phiw_h * phiw_h_9 + b_pliw_l * pliw_l_9
10 alt10 av b_dur_nc * dur_nc_10 + b_pmiw_m * pmiw_m_10 + b_pmnwmj * pmnwmj_10 + b_phiw_h * phiw_h_10 + b_pliw_l * pliw_l_10

[Model]
$MNL

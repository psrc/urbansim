GET DATA  /TYPE = TXT
 /FILE = 'N:\PSRC\dev_constr\parcels_merged.tab'
 /DELCASE = LINE
 /DELIMITERS = "\t"
 /ARRANGEMENT = DELIMITED
 /FIRSTCASE = 1
 /IMPORTCASE = ALL
 /VARIABLES =
 id_parcel A28
 bgusecd A23
 bgsf F6.2
 stories F8.2
 ftprint F6.2
 yrblt F4.2
 nunits F1.0
 bedrms F1.0
 bathfull F1.0
 bath3qtr F1.0
 bathhalf F1.0
 bathrms F4.2
 bgusedes A154
 gencateg A61
 nbldgs F2.1
 nobldgs F1.0
 du_sfr F5.0
 du_mfr F5.0
 sf_sfr F9.0
 sf_mfr F9.0
 sf_com F9.0
 sf_gov F9.0
 sf_ind F9.0
 inurbctr A2
 genuse A3
 cplanid F5.0
 desc A34
 minresd A2
 maxresd A2
 lot_ac F7.2
 lot_sf F10.0
 .
CACHE.
EXECUTE.

VARIABLE LABELS
	id_parcel 'County/Parcel ID'
	bgusecd 'Building Use Code'
	bgsf 'Building Floor Area'
	stories 'Number of Stories'
	ftprint 'Footprint in sqft'
	yrblt 'Latest Year Built'
	nunits 'Number of Dwelling Units'
	bedrms 'Number of Bedrooms'
	bathfull 'Number of Full Baths'
	bath3qtr 'Number of 3-Quarter Baths'
	bathhalf 'Number of Half Baths'
	bathrms 'Total Number of Bathrooms'
	bgusedes 'Building Use Descriptions'
	gencateg 'Generic Building Use Categories'
	nbldgs 'Number of Buildings'
	nobldgs 'Number of Outbuildings'
	du_sfr 'Single Family Dwelling Units'
	du_mfr 'Multi-Family Dwelling Units'
	sf_sfr 'Floor Area of Single Family Residential'
	sf_mfr 'Floor Area of Multi-Family Residential'
	sf_com 'Floor Area of Commercial'
	sf_gov 'Floor Area of Governmental'
	sf_ind 'Floor Area of Industrial'
	inurbctr 'In Urban Center'
	genuse 'Generic Land Use Category'
	cplanid 'Comprehensive Plan ID'
	desc 'Land Use Description'
	minresd 'Minimum Residential Density'
	maxresd 'Maximum Residential Density'
	lot_ac 'Lot Size in Acres'
	lot_sf 'Lot Size in Sqft' .
EXECUTE .

VALUE LABELS cplanid
	9  "Agriculture"
	10 "Airport"
	11 "Aviation Business Center"
	12 "Airport Industrial"
	13 "Auto Oriented Commercial"
	17 "Buffer"
	20 "Office Park"
	22 "Business/Industrial Park"
	25 "Center Office Residential"
	26 "Center Suburban"
	36 "Civic-Educational"
	38 "Commercial"
	39 "Commercial/Recreation"
	42 "Commercial Medium Intensity"
	44 "Commercial, Industrial, Agricultur"
	48 "Commercial/Light Industrial"
	49 "Mixed Use Town Center"
	50 "Commercial/Mixed Use"
	52 "Commerical / Housing"
	53 "Common Wall Single Family (12)"
	54 "Common Wall Single Family (9)"
	56 "Community Facility"
	57 "Community Commercial"
	60 "Utility"
	62 "Constrained Residential"
	63 "Convenience Commercial"
	65 "Corridor Commercial"
	66 "Single Family 1du/ac"
	68 "Residential 4-12 Unit/Acre"
	70 "Design District"
	71 "Forest Land"
	74 "Central Business District"
	76 "Downtown Residential Districts"
	77 "Duplex, Mobile Home,Single Family"
	87 "Evergreen Highlands JPA"
	88 "Fairgrounds"
	93 "Government"
	94 "Heavy Commercial"
	96 "Heavy Industrial"
	99 "High Density Multifamily"
	100 "High Density Residential DD"
	112 "Industrial"
	114 "Industrial Tourist District Ov"
	116 "Intensity 1 (Residential)"
	124 "Large Lot Residential"
	125 "Light Commercial"
	126 "Light Industrial"
	131 "Light Manufacturing"
	132 "Commercial Low Intensity"
	135 "Local Business"
	137 "Low Density Multifamily"
	139 "Low Density Res 2 Transit Ovly"
	140 "Low Density Residential"
	150 "Low Urban Density Residential"
	153 "Manufacturing Center"
	157 "Master Planned Community"
	160 "Medical Facilities"
	162 "Medium Density Multifamily"
	171 "Mid-Rise Office District"
	177 "High Density Residential Mixed"
	178 "Mixed Medium Density Residential/C"
	180 "Mixed Single and Multi-Family"
	185 "MIxed Use"
	186 "Mixed Use Office"
	187 "Mixed Use Planned Development"
	190 "Mixed, Limited Multifamily"
	191 "Mobile Home Park"
	193 "Moderate Density Single Family"
	194 "Moderate Urban Density"
	195 "Mt Rainier Vista SPA"
	196 "Muckleshoot Tribe of Indians"
	201 "Multi-Family (36)"
	204 "Multifamily Residential"
	209 "Multi Family Residential 12-24du/a"
	210 "Multi Family Residential 8-12du/ac"
	213 "Multifamily High Mixed Use 29du-ac"
	217 "Medium Density Residential Mix"
	221 "Neighborhood Commercial"
	228 "Office"
	229 "Office / Residential"
	233 "Office/Multi-Family"
	240 "Park - Multi-Family Medium Density"
	241 "Park - Single Family High Density"
	243 "Park - Single Family Medium Densit"
	251 "Parks/Open Space"
	254 "Pedestrian Oriented Commercial"
	257 "Residential Planned Neighborhood"
	259 "Potential Annexation Area"
	262 "Private Open Space"
	264 "Public/Institutional"
	269 "Public & Quasi-Public"
	271 "Public Facility - Multi-Family Med"
	272 "Public Facility - Office"
	274 "Public Facility - Single Family Hi"
	275 "Public Facility - Single Family Me"
	285 "Public/Institutional Mixed-Use"
	292 "R-30 (30000 sq ft)"
	293 "R-40 Single Dwelling Unit"
	299 "Regional Commercial"
	305 "Residential"
	307 "Residential 6-10du/ac"
	309 "Residential 2 (15,000 Sq. Ft.-8,40"
	314 "Residential 2-5du/ac, Office-Prof,"
	319 "Single Family 5du/ac"
	321 "Residential 6-10du/ac, Office-Prof"
	322 "Residential-Agriculture"
	323 "Residential Commercial Center"
	334 "R-20 Single Dwelling Unit"
	335 "Residential Reserve"
	339 "Residential Urban"
	344 "Retirement Facility"
	345 "Transit Facility"
	350 "Acitvity Center"
	357 "Rural Protection"
	358 "Residential Rural"
	359 "Ruston Planned Development"
	360 "Sand Point Reuse Area"
	362 "School"
	366 "Sensitive"
	369 "Mixed Residential 7.26du-ac"
	375 "Single Family 2du/ac"
	376 "Single Family 3du/ac"
	381 "Single Family Estates 1.24du-ac"
	383 "High Density Residential"
	384 "Single Family Institution"
	386 "Single Family Low Density"
	388 "Medium Density Res. Tourist Di"
	392 "Single Family Residential"
	393 "Single Family High Density"
	398 "Single Family Urban Residential"
	400 "Residential 11-15du/ac"
	401 "Single Family, R-8.4"
	403 "Special Study Area"
	405 "Stuck River SPA"
	406 "Study Area"
	407 "Residential Suburban"
	411 "Tukwila Valley South"
	412 "Urban Growth Area"
	413 "Urban Growth Reserve"
	414 "Urban Housing Densities"
	415 "Urban Village"
	418 "Water/Right of Way"
	419 "Waterfront".

SAVE OUTFILE='N:\PSRC\dev_constr\parcels_merged.sav'
  /COMPRESSED.
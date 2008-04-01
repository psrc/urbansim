
from opus_core import misc

ds = er.estimator.get_data_as_dataset(3)
misc.corr(ds.get_attribute("year_built"),
          ds.get_attribute("empden"),
          ds.get_attribute("far"),
          ds.get_attribute("gcdacbd"),
          ds.get_attribute("ln_land"),
          ds.get_attribute("lnemp30da"),
          ds.get_attribute("lnsqft"))
          
ds = er.estimator.get_data_as_dataset(4)
misc.corr(ds.get_attribute("far"),
          ds.get_attribute("gcdacbd"),
          ds.get_attribute("lnbedsqft"),
          ds.get_attribute("lnemp10wa"),
          ds.get_attribute("lnemp30tw"),
          ds.get_attribute("lnsqftunit"))

ds = er.estimator.get_data_as_dataset(8)
misc.corr(ds.get_attribute("year_built"),
          ds.get_attribute("lnemp30da"),
          ds.get_attribute("lnsqft"))

ds = er.estimator.get_data_as_dataset(10)
misc.corr(ds.get_attribute("lnemp10da"),
          ds.get_attribute("lnemp10wa"),
          ds.get_attribute("lnsqft"))

ds = er.estimator.get_data_as_dataset(12)
misc.corr(ds.get_attribute("beds"),
          ds.get_attribute("gcdacbd"),
          ds.get_attribute("lnbedsqft"),
          ds.get_attribute("lnemp10wa"),
          ds.get_attribute("lnemp30tw"),
          ds.get_attribute("lnempden"),
          ds.get_attribute("lnsqftunit"))

ds = er.estimator.get_data_as_dataset(13)
misc.corr(ds.get_attribute("year_built"),
          ds.get_attribute("empden"),
          ds.get_attribute("gcdacbd"),
          ds.get_attribute("hirise15"),
          ds.get_attribute("ln_land"),
          ds.get_attribute("lnemp30da"),
          ds.get_attribute("lnsqft"))

ds = er.estimator.get_data_as_dataset(19)
misc.corr(ds.get_attribute("gcdacbd"),
          ds.get_attribute("lnbedsqft"),
          ds.get_attribute("lnemp10wa"),
          ds.get_attribute("lnemp30tw"),
          ds.get_attribute("lnempden"),
          ds.get_attribute("lnlotsqft"),
          ds.get_attribute("lnsqftunit"),
          ds.get_attribute("preww2"),
          ds.get_attribute("yrblt10"))

ds = er.estimator.get_data_as_dataset(20)
misc.corr(ds.get_attribute("year_built"),
          ds.get_attribute("gcdacbd"),
          ds.get_attribute("ln_land"),
          ds.get_attribute("lnemp30da"),
          ds.get_attribute("lnsqft"))

ds = er.estimator.get_data_as_dataset(21)
misc.corr(ds.get_attribute("year_built"),
          ds.get_attribute("empden"),
          ds.get_attribute("far"),
          ds.get_attribute("gcdacbd"),
          ds.get_attribute("lnemp30da"),
          ds.get_attribute("lnsqft"))

ds = er.estimator.get_data_as_dataset(23)
misc.corr(ds.get_attribute("gcdacbd"),
          ds.get_attribute("lnemp10wa"),
          ds.get_attribute("lnemp20da"),
          ds.get_attribute("lnemp30tw"),
          ds.get_attribute("lnempden"),
          ds.get_attribute("lnlotsqft"))

gcdacbd
lnemp10wa
lnemp20da
lnemp30tw
lnempden
lnlotsqft



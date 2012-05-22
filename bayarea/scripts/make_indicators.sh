python -m urbansim.tools.make_indicators -x /workspace/opus/project_configs/bay_area_parcel_unit_price.xml -c /workspace/opus/data/bay_area_parcel/runs/run_138.2012_05_15_16_53 -i regional_indicators -y "range(2010,2036)"
python -m urbansim.tools.make_indicators -x /workspace/opus/project_configs/bay_area_parcel_unit_price.xml -c /workspace/opus/data/bay_area_parcel/runs/run_138.2012_05_15_16_53 -i county_indicators -y "range(2010,2036)"
python -m urbansim.tools.make_indicators -x /workspace/opus/project_configs/bay_area_parcel_unit_price.xml -c /workspace/opus/data/bay_area_parcel/runs/run_139.2012_05_15_21_23/ -i regional_indicators -y "range(2010,2036)"
python -m urbansim.tools.make_indicators -x /workspace/opus/project_configs/bay_area_parcel_unit_price.xml -c /workspace/opus/data/bay_area_parcel/runs/run_139.2012_05_15_21_23/ -i county_indicators -y "range(2010,2036)"

cd /workspace/opus/data/bay_area_parcel/runs
zip indicators138_139_2025.zip /workspace/opus/data/bay_area_parcel/runs/run_139.2012_05_15_21_23/indicators/*_2010-2035* /workspace/opus/data/bay_area_parcel/runs/run_138.2012_05_15_16_53/indicators/*_2010-2035*

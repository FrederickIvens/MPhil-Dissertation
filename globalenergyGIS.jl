using CSV
using DataFrames
using PyCall
using Dates



using GlobalEnergyGIS
saveconfig("D:/GISdata", 12345, "abcdef123-ab12-cd34-ef56-abcdef123456", agree_terms=true)
download_datasets()
rasterize_datasets(cleanup=:all)
download_and_convert_era5(2023)
maketempera5(2023)
create_scenario_datasets("SSP2", 2050)
predictdemand(gisregion="Europe8", sspscenario="ssp2-26", sspyear=2050, era_year=2023)
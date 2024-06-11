from capacityfactors import res_capacity

cutoutpath = '/Volumes/fi246disk/cutouts/global-2023-jan-dec-era5-hourly.nc'
regions = ["middle_east", "north_america", "europe", "latin_america", "north_asia", "south_asia", "north_west_asia", "south_west_asia", "ups", "north_africa", "africa", "atlantic_north"]
carriers = ["wind", "pv"]
for region in regions:
    for carrier in carriers:
        res_capacity(filepath=cutoutpath, gisregion=region, carrier=carrier, year=2023)
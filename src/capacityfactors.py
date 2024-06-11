import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
import atlite
import logging
import cartopy.io.shapereader as shpreader
from regiondefinitions import regions_dic
logging.basicConfig(level=logging.INFO)

def all_countries():
    shpfilename = shpreader.natural_earth(
        resolution="10m", category="cultural", name="admin_0_countries"
    )
    reader = shpreader.Reader(shpfilename)
    all_countries = gpd.GeoDataFrame(
        {'geometry': [r.geometry for r in reader.records()], 'country': [r.attributes['NAME_EN'] for r in reader.records()]},
        crs="EPSG:4326"
    )
    return all_countries

def get_countries(region: str, dictionary: dict = regions_dic):
    for _, value in dictionary.items():
        if value["region"] == region:
            return value['countries']
    raise ValueError("Region not in dictionary.")

def res_capacity(filepath: str, gisregion: str, carrier: str, year: int):
    cutout = atlite.Cutout(path=filepath)
    countries = get_countries(gisregion)
    all_regions = all_countries()
    region = all_regions[all_regions['country'].isin(countries)]
    region_bounds = region.total_bounds
    region_cutout = cutout.sel(bounds=region_bounds)
    print(f"Calculating {carrier} capacity factors for {gisregion}...")
    if carrier == "wind":
        path_to_nc = f'/Volumes/fi246disk/wind_cap_f/wind-cap-factors-{gisregion}-{year}-jan-dec-hourly.nc'
        wind = region_cutout.wind( 
            turbine="Vestas_V112_3MW", 
            shapes=region['geometry'],
            per_unit=True
        )
        wind.to_netcdf(path_to_nc)
        print(f'Wind capacity factors for {region} saved to: {path_to_nc}')
        return 
    
    elif carrier == "pv":
        path_to_nc = f'/Volumes/fi246disk/solar_cap_f/pv-cap-factors-{gisregion}-{year}-jan-dec-hourly.nc'
        pv = region_cutout.pv(
            panel='CSi',
            orientation="latitude_optimal",
            shapes=region['geometry'],
            per_unit=True
        )
        pv.to_netcdf(path_to_nc)
        print(f'PV capacity factors for {region} saved to: {path_to_nc}')
        return 
    
    else:
        raise ValueError("Invalid carrier. Available: \"wind\"; \"pv\".")
import geopandas as gpd
import numpy as np
import math
import pandas as pd
import atlite
import cartopy.io.shapereader as shpreader
from shapely.ops import unary_union
from regiondefinitions import regions_dic, region_crs
import h5py
from shapely.geometry import box
from pathlib import Path
import os
import xarray as xr
import matplotlib.pyplot as plt
import random
import matplotlib.colors as mcolors
import pickle


def get_countries(region: str, dictionary: dict = regions_dic):
      for key, value in dictionary.items():
            if key == region:
                  return value['countries']
      raise ValueError("Region not in dictionary.")

def region_area(gisregion: int):
      countries = get_countries(gisregion)
      all_regions = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
      region = all_regions[all_regions['name'].isin(countries)]
      region = region.to_crs(epsg=5070)
      areas = region.geometry.area.values
      total_area = sum(areas)
      return total_area

def syntheticdemand_gis(path: str, gisregion: str, sspscenario: str, era_year: int = 2018, year: int=2050):
      sspscenarios = (
        "ssp1-19", "ssp1-26", "ssp1-34", "ssp1-45",
        "ssp2-26", "ssp2-34", "ssp2-45",
        "ssp3-34", "ssp3-45"
)
      if sspscenario not in sspscenarios:
            raise ValueError(f"Invalid SSP scenario: {sspscenario}. Allowed values are: {', '.join(sspscenarios)}.")
      filepath = Path(path) / f"{sspscenario}-{year}" / f"SyntheticDemand_{gisregion}_{sspscenario}-{year}_{era_year}.csv"
      if not filepath.is_file():
            raise ValueError(f"File not found: {filepath}")
      try: 
            df = pd.read_csv(filepath)
      except Exception as e:
            print(f"File could not be read: {e}")

      start_datetime = pd.Timestamp(f'{year}-01-01 00:00:00')
      end_datetime = pd.Timestamp(f'{year}-12-31 23:00:00')
      time_index = pd.date_range(start=start_datetime, end=end_datetime, freq='h')
      df.index = time_index
      series = df.sum(axis=1)
      series.name = 'demand'
      
      return series
                    
def historic_demand(path: str, year: int, multiplier: int, sspscenario: str = None):
      df = pd.read_csv(Path(path), index_col=0, parse_dates=True)
      df.index = df.index.map(lambda x: x.replace(year=2050))
      series = df['Total_Demand']
      return series

def region_plotting(gisregion: str, countries: list):
      all_regions = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
      region = all_regions[all_regions['name'].isin(countries)]

      colors = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
      random.shuffle(colors)

      fig, ax = plt.subplots(figsize=(20, 10))  
      region.plot(ax=ax, edgecolor='k', color=[colors[i % len(colors)] for i in range(len(region))])

      ax.set_title(f'{gisregion} Plot')
      plt.show()

def check_countries():
      all_region_countries = []
      for key, value in regions_dic.items():
            all_countries = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
            countries = regions_dic[key]["countries"]
            all_region_countries += countries.copy()
            difference = list(set(countries) - set(all_countries['name']))
            region = all_countries[all_countries['name'].isin(countries)]
            region_countries = len(region['name'])
            total_difference = list(set(all_countries['name']) - set(all_region_countries))
            print(total_difference)

def check_pickle(path: str, gisregion: str, carrier: str, year: int, density: int = 1.0, land_available: int = 1.0, resolution: float = 2.0):
      filepath = f"{path}/{carrier}_cap_f_granularity_{resolution}/{carrier}_capacity_factors_{gisregion}_{year}_gran_{resolution}.pkl"
      with open(filepath, 'rb') as f:
            dfs = pickle.load(f) 
      print(dfs)

def vre_gen_potential_atlite_granularity(path: str, gisregion: str, carrier: str, year: int, density: int = 1.0, land_available: int = 1.0, resolution: float = 2.0):
      filepath = f"{path}/{carrier}_cap_f_granularity_{resolution}/{carrier}_capacity_factors_{gisregion}_{year}_gran_{resolution}.pkl"
      with open(filepath, 'rb') as f:
            dfs = pickle.load(f)
      print(f"Data loaded successfully for {gisregion}. Number of items in dfs: {len(dfs)}")
      start_datetime = pd.Timestamp(f'2050-01-01 00:00:00')
      end_datetime = pd.Timestamp(f'2050-12-31 23:00:00')
      time_index = pd.date_range(start=start_datetime, end=end_datetime, freq='h')

      cf_combined = pd.DataFrame(index=time_index)
      caps = []

      for key, df in dfs.items():
            cf_series = df['mean_cf'].reset_index(drop=True)
            cf_series.index = time_index[:len(cf_series)]
            cf_combined[key] = cf_series
            area = df['total_area'].iloc[0]
            cap = area * density * land_available * 1E-06  # MW
            caps.append(cap)
      caps_df = pd.Series(caps, index=cf_combined.columns)
      return cf_combined.copy(), caps_df

def vre_gen_potential_atlite_granularity_total(path: str, gisregion: str, carrier: str, year: int, resolution, density: int = 1.0, land_available: int = 1.0):
      filepath = f"{path}/{carrier}_cap_f_granularity_{resolution}/{carrier}_capacity_factors_{gisregion}_{year}_gran_{resolution}.pkl"
      start_datetime = pd.Timestamp(f'2050-01-01 00:00:00')
      end_datetime = pd.Timestamp(f'2050-12-31 23:00:00')
      time_index = pd.date_range(start=start_datetime, end=end_datetime, freq='h')
      with open(filepath, 'rb') as f:
            df = pickle.load(f) 

      cf_series = df['mean_cf']
      cf_series = df['mean_cf'].reset_index(drop=True)
      cf_series.index = time_index[:len(cf_series)] 
      area = df['total_area'].iloc[0]
      print(f'{gisregion}: area: {area:.2e}')
      cap = area * density * land_available * 1E-06 # MW
      return cf_series, cap


def renewable_potential_atlite_total(gisregion: str, carrier: str, year: int, cutoutpath: str, outputpath: str, resolution: str = 'total'):
    wind_path = f'{outputpath}/wind_cap_f_granularity_{resolution}'
    pv_path = f'{outputpath}/pv_cap_f_granularity_{resolution}'
    os.makedirs(wind_path, exist_ok=True)
    os.makedirs(pv_path, exist_ok=True)
    cutout = atlite.Cutout(path=cutoutpath)
    countries = get_countries(gisregion)
    all_regions = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    region = all_regions[all_regions['name'].isin(countries)]
    region.to_crs(epsg=4326)
    crs_system = region_crs[gisregion]
    combined_bounds = unary_union(region['geometry'])
    multipoly = combined_bounds.geoms
    region_areas = [gpd.GeoSeries([poly], crs=4326).to_crs(epsg=crs_system).area.values[0] for poly in multipoly]
    region_area_total = sum(region_areas)
    
    mean_cfs = []
    regions_areas_considered = []
    for j, poly in enumerate(multipoly):
        poly_bounds = poly.bounds
        minlon0 = poly_bounds[0]
        maxlon0 = poly_bounds[2]
        minlat0 = poly_bounds[1]
        maxlat0 = poly_bounds[3]
        length_lon = abs(minlon0 - maxlon0)
        length_lat = abs(minlat0 - maxlat0)
        print(length_lon, length_lat)
        if length_lon <= 1 or length_lat <= 1:
            print('Polygon too small, skipping.')
            continue
        regions_areas_considered.append(region_areas[j])
        region_cutout = cutout.sel(bounds=poly_bounds)
        shape = region_cutout.grid[region_cutout.grid.intersects(poly)]
        ax = region.plot(color='blue', edgecolor='black', alpha=0.5, figsize=(5, 5))
        shape.plot(ax=ax, color='red', edgecolor='black', alpha=0.5)
        print(f"Calculating {carrier} capacity factors for {gisregion}_{j}...")
        if carrier == "wind":
            wind = region_cutout.wind( 
                    turbine="Vestas_V112_3MW", 
                    shapes=shape,
                    per_unit=True
            )
            mean_cf = wind.mean(dim='dim_0')
            mean_cfs.append(mean_cf)
        elif carrier == "pv":
            pv = region_cutout.pv(
                    panel='CSi',
                    orientation="latitude_optimal",
                    shapes=shape,
                    per_unit=True
            )
            mean_cf = pv.mean(dim='dim_0')
            mean_cfs.append(mean_cf)
        else:
            raise ValueError("Invalid carrier. Available.")

    weighted_mean_cf = sum([cf * regions_areas_considered[i] for i, cf in enumerate(mean_cfs)]) / sum(regions_areas_considered)
    weighted_mean_cf_df = weighted_mean_cf.to_dataframe(name=f'mean_cf')
    weighted_mean_cf_df[f'total_area'] = region_area_total      
    print(weighted_mean_cf_df.head())
    output_pickle_path = f'D:/{carrier}_cap_f_granularity_{resolution}/{carrier}_capacity_factors_{gisregion}_{year}_gran_{resolution}.pkl'
    with open(output_pickle_path, 'wb') as f:
        pickle.dump(weighted_mean_cf_df, f)
    print(f"File saved to {output_pickle_path}")
cutoutpath = 'D:/FinishedCutouts/global-2022-jan-dec-era5-hourly.nc'
#renewable_potential_atlite_total(gisregion='europe', carrier='wind', year=2022, cutoutpath=cutoutpath, outputpath='D:')

def vre_gen_potential_atlite_granularity_2(path: str, gisregion: str, carrier: str, year: int, resolution, density: int = 1.0, land_available: int = 1.0):
      filepath = f"{path}/{carrier}_cap_f_granularity_{resolution}/{carrier}_capacity_factors_{gisregion}_{year}_gran_{resolution}.pkl"
      with open(filepath, 'rb') as f:
            dfs = pickle.load(f)
      print(f"Data loaded successfully for {gisregion}. Number of items in dfs: {len(dfs)}")
      start_datetime_1 = pd.Timestamp(f'{year}-01-01 00:00:00')
      end_datetime_1 = pd.Timestamp(f'{year}-12-31 23:00:00')
      time_index_1 = pd.date_range(start=start_datetime_1, end=end_datetime_1, freq='h')
      start_datetime_2 = pd.Timestamp(f'2050-01-01 00:00:00')
      end_datetime_2 = pd.Timestamp(f'2050-12-31 23:00:00')
      time_index_2 = pd.date_range(start=start_datetime_2, end=end_datetime_2, freq='h')

      cf_combined = pd.DataFrame(index=time_index_2)
      caps_list = []

      for key, value in dfs.items():
            cf_combined[key] = value[0]
            area = value[1]
            caps = area * density * land_available * 1E-06  # MW
            caps_list.append(caps)
      # Concatenate all series into a single DataFrame
      caps_combined = pd.concat(caps_list, axis=1)
      print(f'{gisregion} {carrier} has {caps_combined.shape[1]} cells.')
      return cf_combined.copy(), caps_combined.copy()
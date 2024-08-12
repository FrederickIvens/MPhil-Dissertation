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

def vre_gen_potential_atlite_granularity(gisregion: str, carrier: str, year: int, density: int = 1.0, land_available: int = 1.0, resolution: float = 2.0):
      filepath = f"/Volumes/fi246disk/Atlite/{carrier}_cap_f_granularity_{resolution}/{carrier}_capacity_factors_{gisregion}_{year}_gran_{resolution}.pkl"
      with open(filepath, 'rb') as f:
            dfs = pickle.load(f) 
      start_datetime = pd.Timestamp(f'2050-01-01 00:00:00')
      end_datetime = pd.Timestamp(f'2050-12-31 23:00:00')
      time_index = pd.date_range(start=start_datetime, end=end_datetime, freq='h')
      cfs = []
      caps = []
      for key, df in dfs.items():
            if gisregion == 'ups':
                  print(key)
            cf_series = df['mean_cf']
            cf_series = df['mean_cf'].reset_index(drop=True)
            cf_series.index = time_index[:len(cf_series)] 
            cfs.append(cf_series)
            area = df['total_area'].iloc[0] 
            cap = area * density * land_available * 1E-06 # MW
            caps.append(cap)
      return cfs, caps

def vre_gen_potential_atlite_granularity_total(gisregion: str, carrier: str, year: int, resolution, density: int = 1.0, land_available: int = 1.0):
      filepath = f"/Users/frederickivens/Documents/MPhil_Energy_Technologies/Dissertation_Project/Codes/data/supply/{carrier}_cap_f_granularity_{resolution}/{carrier}_capacity_factors_{gisregion}_{year}_gran_{resolution}.pkl"
      start_datetime = pd.Timestamp(f'2050-01-01 00:00:00')
      end_datetime = pd.Timestamp(f'2050-12-31 23:00:00')
      time_index = pd.date_range(start=start_datetime, end=end_datetime, freq='h')
      with open(filepath, 'rb') as f:
            df = pickle.load(f) 

      cf_series = df['mean_cf']
      cf_series = df['mean_cf'].reset_index(drop=True)
      cf_series.index = time_index[:len(cf_series)] 
      area = df['total_area'].iloc[0]
      cap = area * density * land_available * 1E-06 # MW
      return cf_series, cap


import geopandas as gpd
import numpy as np
import pandas as pd
import atlite
import cartopy.io.shapereader as shpreader
from regiondefinitions import regions_dic
import h5py
from pathlib import Path
import xarray as xr

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

def res_capacity_atlite(filepath: str, gisregion: str, carrier: str, year: int):
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
        print(f'Wind capacity factors for {gisregion} saved to: {path_to_nc}')
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
        print(f'PV capacity factors for {gisregion} saved to: {path_to_nc}')
        return 
    
    else:
        raise ValueError("Invalid carrier. Available: \"wind\"; \"pv\".")
    
def vre_gen_potential(gisregion: str, carrier: str, year: int, density: int = 1.0, land_available: int = 1.0):
     filepath = f"/Volumes/fi246disk/{carrier}_cap_f/{carrier}-cap-factors-{gisregion}-{year}-jan-dec-hourly.nc"
     ds = xr.open_dataset(filepath)
     time_index = pd.date_range(start="2050-01-01", end="2050-12-31", freq="h")
     series = pd.Series(ds.values, index=time_index)
     return series * density * land_available



def syntheticdemand_gis(path: str, region: str, sspscenario: str, era_year: int = 2018, year: int=2050):
      sspscenarios = (
        "ssp1-19", "ssp1-26", "ssp1-34", "ssp1-45",
        "ssp2-26", "ssp2-34", "ssp2-45",
        "ssp3-34", "ssp3-45"
)
      if sspscenario not in sspscenarios:
            raise ValueError(f"Invalid SSP scenario: {sspscenario}. Allowed values are: {', '.join(sspscenarios)}.")
      filepath = Path(path) / f"{sspscenario}-{year}" / f"SyntheticDemand_{region}_{sspscenario}-{year}_{era_year}.csv"
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

def vres_capacity_gis(path: str, region: str, carrier: str, sspscenario: str, era_year: int = 2018, year: int=2050):
      c = carrier[:4] if carrier != "solar" else carrier
      filepath = Path(path) / f"GIS{c}{era_year}"/ f"GISdata_{c}{era_year}_{sspscenario.lower()}_{region}.mat"
      if not filepath.is_file():
            raise ValueError(f"File not found: {filepath}")
      
      if carrier == "solar":
            try: 
                  with h5py.File(filepath, 'r') as file:
                        CFtime_pvplantA = file['CFtime_pvplantA'][:]
                        CFtime_pvplantB = file['CFtime_pvplantB'][:]
                        CFtime_pvrooftop = file['CFtime_pvrooftop'][:]
                        capacity = CFtime_pvplantA + CFtime_pvplantB + CFtime_pvrooftop
            except Exception as e:
                  print(f"File could not be read: {e}")

      elif carrier == "windonshore":
            try: 
                  with h5py.File(filepath, 'r') as file:
                        CFtime_windonshoreA = file['CFtime_windonshoreA'][:]
                        CFtime_windonshoreB = file['CFtime_windonshoreB'][:]
                        capacity = CFtime_windonshoreA + CFtime_windonshoreB
            except Exception as e:
                  print(f"File could not be read: {e}")

      elif carrier == "windoffshore":
            try: 
                  with h5py.File(filepath, 'r') as file:
                        CFtime_windoffshore = file['CFtime_windoffshore'][:]
                        capacity = CFtime_windoffshore
            except Exception as e:
                  print(f"File could not be read: {e}")

      else:
            raise ValueError("Carrier does not exist. Existing carrier: \"solar\"; \"windonshore\"; \"windoffshore\"")
      print("carrier", capacity)
      capacity_total = np.sum(capacity, axis=(0, 1))
      start_datetime = pd.Timestamp(f'{year}-01-01 00:00:00')
      end_datetime = pd.Timestamp(f'{year}-12-31 23:00:00')
      time_index = pd.date_range(start=start_datetime, end=end_datetime, freq='h')
      series = pd.Series(capacity_total, index=time_index, name='total_capacity')

      return series
                    
def historic_demand(path: str, year: int, sspscenario: str = None):
    df = pd.read_csv(Path(path), index_col=0, parse_dates=True)
    df.index = df.index.map(lambda x: x.replace(year=2050))
    series = df['Total_Demand']
    return series
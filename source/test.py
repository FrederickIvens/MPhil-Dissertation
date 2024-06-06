import subprocess
import sys
import bottleneck
import cdsapi
import dask
import geopandas as gpd
import netCDF4
import numexpr
import numpy as np
import pandas as pd
import tqdm
import rasterio
import rtree
import scipy
import shapely
import xarray as xr
import atlite
import logging
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os
import time
import ctypes

# Constants for Windows sleep prevention
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

# Prevent the system from sleeping
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the global bounds using unary_union of all countries
shpfilename = shpreader.natural_earth(
    resolution="10m", category="cultural", name="admin_0_countries"
)
reader = shpreader.Reader(shpfilename)
all_countries = gpd.GeoDataFrame(
    {'geometry': [r.geometry for r in reader.records()], 'country': [r.attributes['NAME_EN'] for r in reader.records()]},
    crs="EPSG:4326"
)

# Calculate the combined bounds of all countries
combined_bounds = all_countries.unary_union.bounds

# Define the time periods of interest with hourly resolution
time_range_1 = pd.date_range("2023-01-01", "2023-06-30 23:00:00", freq="h")
time_range_2 = pd.date_range("2023-07-01", "2023-12-31 23:00:00", freq="h")

# Define the base paths to the external hard drives
base_path_1 = 'D:\Cutouts'  # Adjust this path to your first external hard drive
base_path_2 = 'E:\cutouts2'  # Adjust this path to your second external hard drive

# Create the directories if they don't exist
os.makedirs(base_path_1, exist_ok=True)
os.makedirs(base_path_2, exist_ok=True)

def prepare_cutout(time_range, base_path, filename):
    try:
        # Create the cutout for the given time range and base path
        cutout = atlite.Cutout(
            path=os.path.join(base_path, filename),  # Path where the cutout file will be saved
            module="era5",                           # The weather data source
            bounds=combined_bounds,                  # The combined geographical bounds for all countries
            time=time_range                          # The time range with hourly resolution
        )

        # Prepare the cutout
        logger.info(f"Preparing cutout for time range {time_range[0]} to {time_range[-1]}")
        cutout.prepare()
        logger.info(f"Successfully prepared cutout for time range {time_range[0]} to {time_range[-1]}")

    except Exception as e:
        logger.error(f"Failed to prepare cutout for time range {time_range[0]} to {time_range[-1]}: {e}")
        raise

def main():
    success_1 = False
    success_2 = False

    while not success_1:
        try:
            prepare_cutout(time_range_1, base_path_1, 'global-2023-jan-jun-era5-hourly.nc')
            success_1 = True
        except Exception as e:
            logger.error(f"Error preparing cutout for Jan-Jun, retrying in 10 seconds...")
            time.sleep(10)  # Wait before retrying

    while not success_2:
        try:
            prepare_cutout(time_range_2, base_path_2, 'global-2023-jul-dec-era5-hourly.nc')
            success_2 = True
        except Exception as e:
            logger.error(f"Error preparing cutout for Jul-Dec, retrying in 10 seconds...")
            time.sleep(10)  # Wait before retrying

if __name__ == '__main__':
    main()
    # Reset the sleep settings when the script is done
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    print("Cutouts prepared and stored on the external hard drives")

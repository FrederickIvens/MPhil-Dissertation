import numpy as np 
import h5py
import pandas as pd 
from pathlib import Path

sspscenarios = (
        "ssp1-19", "ssp1-26", "ssp1-34", "ssp1-45",
        "ssp2-26", "ssp2-34", "ssp2-45",
        "ssp3-34", "ssp3-45"
)
def syntheticdemand(path: str, region: str, sspscenario: str, era_year: int = 2018, year: int=2050):
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
                    
              
              
        


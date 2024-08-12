GlobalEnergyGIS Setup Guide

GlobalEnergyGIS is a tool written in Julia for generating and analyzing global energy datasets. This guide will walk you through the initial setup and usage.

Prerequisites

Make sure you have Julia installed on your system. If you're using GlobalEnergyGIS for the first time, follow the steps below.

Installation

1. Add the GlobalEnergyGIS package to your Julia environment:
   (@v1.6) pkg> add https://github.com/niclasmattsson/GlobalEnergyGIS

2. Activate the GlobalEnergyGIS environment:
   julia> using Revise
   julia> using Pkg
   julia> Pkg.activate("path_to_folder")  # Replace "path_to_folder" with your desired folder path

3. Load the GlobalEnergyGIS package:
   julia> using GlobalEnergyGIS

Initial Setup

1. Configure the API and folder path:
   julia> saveconfig("D:/GISdata", 12345, "abcdef123-ab12-cd34-ef56-abcdef123456", agree_terms=true)
   - Replace "D:/GISdata" with your folder path.
   - Replace 12345 with your user ID.
   - Replace "abcdef123-ab12-cd34-ef56-abcdef123456" with your API key.

2. Download and process the datasets:
   julia> download_datasets()
   julia> rasterize_datasets(cleanup=:all)
   julia> download_and_convert_era5(2018)

Generating Synthetic Demand Data

Once the initial setup is complete, you can generate synthetic demand data:

1. Open the syntheticdemand_csv() helper function to modify the output path, SSP scenarios, SSP variants, and regions. The region definitions can be found in regiondefinitions.jl.

2. Run the following commands to generate CSV files with demand time series for each region:
   julia> using Revise
   julia> using Pkg
   julia> Pkg.activate("path_to_folder")
   julia> using GlobalEnergyGIS
   julia> syntheticdemand_csv()

Output

The CSV files containing the demand time series for each region should now be generated and saved in the specified output path.

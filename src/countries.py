import geopandas as gpd

# Load the Natural Earth dataset at 10m resolution
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Extract unique country names
natural_earth_countries = set(world['name'].unique())
print("Countries in Natural Earth dataset:")

regions_dic = {
    "north_america": {
        "bus": 1,
        "region": "north_america",
        "coordinates": (-106.5, 38.3),
        "countries": sorted(["Canada", "United States of America", "Mexico"])
    },
    "latin_america": {
        "bus": 2,
        "region": "latin_america",
        "coordinates": (-60.5, -13.3),
        "countries": sorted(["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Cuba", "Dominican Rep.", "Ecuador", "Guatemala", "Haiti", "Honduras", "Paraguay", "Peru", "Uruguay", "Venezuela", "Belize", "Costa Rica", "El Salvador", "Guyana", "Jamaica", "Nicaragua", "Panama", "Suriname", "Trinidad and Tobago"])
    },
    "oceania": {
        "bus": 3,
        "region": "oceania",
        "coordinates": (134.4, -22.6),
        "countries": sorted(["Australia", "New Zealand", "Cook Island", "Fiji", "Tonga", "Tuvalu", "Vanuatu", "New Caledonia", "Papua New Guinea", "Solomon Is."])
    },
    "north_asia": {
        "bus": 4,
        "region": "north_asia",
        "coordinates": (116, 40.1),
        "countries": sorted(["China", "Hong Kong", "Japan", "Mongolia", "South Korea", "Taiwan", "North Korea"])
    },
    "south_asia": {
        "bus": 5,
        "region": "south_asia",
        "coordinates": (114, 0.2),
        "countries": sorted(["Brunei", "Cambodia", "Indonesia", "Laos", "Malaysia", "Myanmar", "Philippines", "Singapore", "Thailand", "Timor-Leste", "Vietnam", "Maldives"])
    },
    "north_west_asia": {
        "bus": 6,
        "region": "north_west_asia",
        "coordinates": (69.7, 48.6),
        "countries": sorted(["Afghanistan", "Azerbaijan", "Kazakhstan", "Kyrgyzstan", "Tajikistan", "Turkmenistan", "Uzbekistan", "Armenia", "Georgia", "Turkey"])
    },
    "south_west_asia": {
        "bus": 7,
        "region": "south_west_asia",
        "coordinates": (74.2, 18.7),
        "countries": sorted(["Bangladesh", "Bhutan", "India", "Nepal", "Pakistan", "Sri Lanka"])
    },
    "middle_east": {
        "bus": 8,
        "region": "middle_east",
        "coordinates": (42.9, 29.7),
        "countries": sorted(["Bahrain", "Iran", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Qatar", "Saudi Arabia", "Syria", "United Arab Emirates", "Yemen", "Azerbaijan", "Georgia", "Turkey", "Armenia", "Cyprus", "Palestine"])
    },
    "europe": {
        "bus": 9,
        "region": "europe",
        "coordinates": (10, 50),
        "countries": sorted(["Albania", "Austria", "Belgium", "Bosnia and Herz.", "Bulgaria", "Croatia", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Montenegro", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "United Kingdom", "Kosovo", "North Macedonia", "Moldova"])
    },
    "ups": {
        "bus": 10,
        "region": "ups",
        "coordinates": (74, 66),
        "countries": sorted(["Belarus", "Russia", "Ukraine"])
    },
    "north_africa": {
        "bus": 11,
        "region": "north_africa",
        "coordinates": (-0.75, 27.5),
        "countries": sorted(["Algeria", "Egypt", "Libya", "Morocco", "Tunisia", "W. Sahara", "Sudan"])
    },
    "africa": {
        "bus": 12,
        "region": "africa",
        "coordinates": (21.6, -14),
        "countries": sorted([
            "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon", 
            "Central African Rep.", "Côte d'Ivoire", "Chad", "Comoros", "Congo", 
            "Dem. Rep. Congo", "Djibouti", "Eq. Guinea", "Eritrea", "eSwatini", "Ethiopia", 
            "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", 
            "Madagascar", "Malawi", "Mali", "Mauritania", "Mozambique", "Namibia", 
            "Niger", "Nigeria", "Rwanda", "São Tomé and Príncipe", "Senegal", "Seychelles", 
            "Sierra Leone", "Somalia", "South Africa", "S. Sudan", "Tanzania", "Togo", 
            "Uganda", "Zambia", "Zimbabwe"])
    },
    "atlantic_north": {
        "bus": 13,
        "region": "atlantic_north",
        "coordinates": (-45, 62),
        "countries": ["Greenland", "Iceland"]
    },
    "alaska": {
        "bus": 14,
        "region": "alaska",
        "coordinates": (-152, 63),
        "countries": []
    }
}

# # Extract countries from regions_dic
# regions_countries = {region: set(details['countries']) for region, details in regions_dic.items()}

# # Combine all countries from regions_dic into a single set
# regions_all_countries = set()
# for countries in regions_countries.values():
#     regions_all_countries.update(countries)

# # Find missing countries in both directions
# missing_in_regions_dic = natural_earth_countries - regions_all_countries
# missing_in_natural_earth = regions_all_countries - natural_earth_countries

# print("\nCountries in Natural Earth dataset that are missing in regions_dic:")
# print(missing_in_regions_dic)

# print("\nCountries in regions_dic that are not in Natural Earth dataset:")
# print(missing_in_natural_earth)

from collections import defaultdict

# Initialize a dictionary to track the occurrences of each country
country_occurrences = defaultdict(list)

# Iterate through the regions_dic and populate the dictionary
for region, details in regions_dic.items():
    for country in details['countries']:
        country_occurrences[country].append(region)

# Identify countries that exist in more than one region
duplicate_countries = {country: regions for country, regions in country_occurrences.items() if len(regions) > 1}

print("Countries that exist in multiple regions:")
for country, regions in duplicate_countries.items():
    print(f"{country} exists in: {regions}")

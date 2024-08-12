# Dictionary containing the regions, coordinates, and countries
regions_dic = {
    "north_america": {
        "bus": 1,
        "region": "North America",
        "coordinates": (-106.5, 38.3),
        "countries": sorted(["Canada", "United States of America", "Mexico"])
    },
    "latin_america": {
        "bus": 2,
        "region": "Latin America",
        "coordinates": (-60.5, -13.3),
        "countries": sorted(["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Cuba", "Dominican Rep.", "Ecuador", "Guatemala", "Haiti", "Honduras", "Paraguay", "Peru", "Puerto Rico", "Uruguay", "Venezuela", "Belize", "Costa Rica", "El Salvador", "Guyana", "Jamaica", "Nicaragua", "Panama", "Suriname", "Trinidad and Tobago"])
    },
    "oceania": {
        "bus": 3,
        "region": "Oceania",
        "coordinates": (134.4, -22.6),
        "countries": sorted(["Australia", "New Zealand", "Cook Island", "Fiji", "Tonga", "Tuvalu", "Vanuatu", "New Caledonia", "Papua New Guinea", "Solomon Is."])
    },
    "north_asia": {
        "bus": 4,
        "region": "North Asia",
        "coordinates": (116, 40.1),
        "countries": sorted(["China", "Hong Kong", "Japan", "Mongolia", "South Korea", "Taiwan", "North Korea"])
    },
    "south_asia": {
        "bus": 5,
        "region": "South Asia",
        "coordinates": (114, 0.2),
        "countries": sorted(["Brunei", "Cambodia", "Indonesia", "Laos", "Malaysia", "Myanmar", "Philippines", "Singapore", "Thailand", "Timor-Leste", "Vietnam", "Maldives"])
    },
    "north_west_asia": {
        "bus": 6,
        "region": "North West Asia",
        "coordinates": (69.7, 48.6),
        "countries": sorted(["Afghanistan", "Azerbaijan", "Kazakhstan", "Kyrgyzstan", "Tajikistan", "Turkmenistan", "Uzbekistan", "Armenia", "Georgia", "Turkey"])
    },
    "south_west_asia": {
        "bus": 7,
        "region": "South West Asia",
        "coordinates": (74.2, 18.7),
        "countries": sorted(["Bangladesh", "Bhutan", "India", "Nepal", "Pakistan", "Sri Lanka"])
    },
    "middle_east": {
        "bus": 8,
        "region": "Middle East",
        "coordinates": (42.9, 29.7),
        "countries": sorted(["Bahrain", "Iran", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Qatar", "Saudi Arabia", "Syria", "United Arab Emirates", "Yemen", "Cyprus", "Palestine"])
    },
    "europe": {
        "bus": 9,
        "region": "Europe",
        "coordinates": (10, 50),
        "countries": sorted(["Albania", "Austria", "Belgium", "Bosnia and Herz.", "Bulgaria", "Croatia", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Montenegro", "Netherlands", "N. Cyprus", "Norway", "Poland", "Portugal", "Romania", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "United Kingdom", "Kosovo", "North Macedonia", "Moldova"])
    },
    "ups": {
        "bus": 10,
        "region": "UPS",
        "coordinates": (74, 66),
        "countries": sorted(["Belarus", "Russia", "Ukraine"])
    },
    "north_africa": {
        "bus": 11,
        "region": "North Africa",
        "coordinates": (-0.75, 27.5),
        "countries": sorted(["Algeria", "Egypt", "Libya", "Morocco", "Tunisia", "W. Sahara", "Sudan", "Somaliland"])
    },
    "africa": {
        "bus": 12,
        "region": "Africa",
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
        "region": "Atlantic North",
        "coordinates": (-45, 62),
        "countries": ["Greenland", "Iceland"]
    },
}

region_crs = {
    "atlantic_north": 32629,  # UTM zone 29N (covers parts of the North Atlantic)
    "africa": 4326,  # Africa Albers Equal Area Conic
    "north_africa": 32634,  # UTM zone 34N
    "ups": 3413,  # NSIDC Sea Ice Polar Stereographic North
    "south_west_asia": 32638,  # UTM zone 38N
    "north_west_asia": 32642,  # UTM zone 42N
    "south_asia": 32643,  # UTM zone 43N
    "north_asia": 32645,  # UTM zone 45N
    "latin_america": 4326,  # South America Albers Equal Area Conic
    "europe": 3035,  # ETRS89 / LAEA Europe
    "north_america": 5070,  # USA Contiguous Albers Equal Area Conic
    "middle_east": 32637,  # UTM zone 37N
    "oceania": 3577,  # GDA94 / Australian Albers
}

# Dictionary to store information about the links 
links_dic = {
    "1_2": {
        "name": "north_america_to_latin_america",
        "bus0": (1, "north_america"),
        "bus1": (2, "latin_america"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "1_10": {
        "name": "north_america_to_ups",
        "bus0": (1, "north_america"),
        "bus1": (10, "ups"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "1_13": {
        "name": "north_america_to_atlantic_north",
        "bus0": (1, "north_america"),
        "bus1": (13, "atlantic_north"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "3_5": {
        "name": "oceania_to_south_asia",
        "bus0": (3, "oceania"),
        "bus1": (5, "south_asia"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "4_5": {
        "name": "north_asia_to_south_asia",
        "bus0": (4, "north_asia"),
        "bus1": (5, "south_asia"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "4_6": {
        "name": "north_asia_to_north_west_asia",
        "bus0": (4, "north_asia"),
        "bus1": (6, "north_west_asia"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "4_7": {
        "name": "north_asia_to_south_west_asia",
        "bus0": (4, "north_asia"),
        "bus1": (7, "south_west_asia"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "4_10": {
        "name": "north_asia_to_ups",
        "bus0": (4, "north_asia"),
        "bus1": (10, "ups"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "5_7": {
        "name": "south_asia_to_south_west_asia",
        "bus0": (5, "south_asia"),
        "bus1": (7, "south_west_asia"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "6_7": {
        "name": "north_west_asia_to_south_west_asia",
        "bus0": (6, "north_west_asia"),
        "bus1": (7, "south_west_asia"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "6_8": {
        "name": "north_west_asia_to_middle_east",
        "bus0": (6, "north_west_asia"),
        "bus1": (8, "middle_east"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "6_10": {
        "name": "north_west_asia_to_ups",
        "bus0": (6, "north_west_asia"),
        "bus1": (10, "ups"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "8_9": {
        "name": "middle_east_to_europe",
        "bus0": (8, "middle_east"),
        "bus1": (9, "europe"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "8_10": {
        "name": "middle_east_to_ups",
        "bus0": (8, "middle_east"),
        "bus1": (10, "ups"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "8_11": {
        "name": "middle_east_to_north_africa",
        "bus0": (8, "middle_east"),
        "bus1": (11, "north_africa"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "8_12": {
        "name": "middle_east_to_africa",
        "bus0": (8, "middle_east"),
        "bus1": (12, "africa"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "9_10": {
        "name": "europe_to_ups",
        "bus0": (9, "europe"),
        "bus1": (10, "ups"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "9_11": {
        "name": "europe_to_north_africa",
        "bus0": (9, "europe"),
        "bus1": (11, "north_africa"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "9_13": {
        "name": "europe_to_atlantic_north",
        "bus0": (9, "europe"),
        "bus1": (13, "atlantic_north"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    },
    "11_12": {
        "name": "north_africa_to_africa",
        "bus0": (11, "north_africa"),
        "bus1": (12, "africa"),
        "length": None,
        "type": "OH",
        "efficiency": 0.0
    }
}

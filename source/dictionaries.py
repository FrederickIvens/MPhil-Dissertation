# Dictionary containing the regions, coordinates, and countries
regions_dic = {
    1: {
        "member": "bus 0",
        "region": "North America",
        "coordinates": (-106.5, 38.3),
        "countries": sorted(["Canada", "USA", "Mexico"])
    },
    2: {
        "member": "bus 1",
        "region": "Latin America",
        "coordinates": (-60.5, -13.3),
        "countries": sorted(["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Cuba", "Dom. Republic", "Ecuador", "Guatemala", "Haiti", "Honduras", "Paraguay", "Peru", "Uruguay", "Venezuela"])
    },
    3: {
        "member": "Bus 3",
        "region": "Oceania",
        "coordinates": (134.4, -22.6),
        "countries": sorted(["Australia", "New Zealand", "Cook Island", "Fiji", "Tonga", "Tuvalu", "Vanuatu"])
    },
    4: {
        "member": "Bus 4",
        "region": "North Asia",
        "coordinates": (116, 40.1),
        "countries": sorted(["China", "Hong-Kong", "Japan", "Mongolia", "South Korea", "Chinese Taipei", "North Korea"])
    },
    5: {
        "member": "Bus 5",
        "region": "South Asia",
        "coordinates": (114, 0.2),
        "countries": sorted(["Brunei", "Cambodia", "Indonesia", "Laos", "Malaysia", "Myanmar", "Philippines", "Singapore", "Thailand", "Timor-Leste", "Vietnam"])
    },
    6: {
        "member": "Bus 6",
        "region": "North West Asia",
        "coordinates": (69.7, 48.6),
        "countries": sorted(["Afghanistan", "Azerbaijan", "Kazakhstan", "Kyrgyzstan", "Tajikistan", "Turkmenistan", "Uzbekistan"])
    },
    7: {
        "member": "Bus 7",
        "region": "South West Asia",
        "coordinates": (74.2, 18.7),
        "countries": sorted(["Bangladesh", "Bhutan", "India", "Maldives", "Nepal", "Pakistan", "Sri Lanka"])
    },
    8: {
        "member": "Bus 8",
        "region": "Middle East",
        "coordinates": (42.9, 29.7),
        "countries": sorted(["Georgia", "Turkey", "Bahrain", "Iran", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Qatar", "Saudi Arabia", "Syria", "UAE", "Yemen", "Azerbaijan"])
    },
    9: {
        "member": "Bus 9",
        "region": "Europe",
        "coordinates": (10, 50),
        "countries": sorted(["Albania", "Austria", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Montenegro", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "United Kingdom"])
    },
    10: {
        "member": "bus 00",
        "region": "UPS",
        "coordinates": (74, 66),
        "countries": sorted(["Belarus", "Russia", "Ukraine"])
    },
    11: {
        "member": "bus 01",
        "region": "North Africa",
        "coordinates": (-0.75, 27.5),
        "countries": sorted(["Algeria", "Egypt", "Libya", "Morocco", "Tunisia", "Israel", "Western Sahara", "Sudan"])
    },
    12: {
        "member": "bus 02",
        "region": "Africa",
        "coordinates": (21.6, -14),
        "countries": sorted(["Angola", "Benin", "Botswana", "Cameroon", "Central African Republic", "Cote d'Ivoire", "Chad", "RDC", "Equatorial Guinea", "Ethiopia", "Gabon", "Gambia", "Ghana", "Kenya", "Lesotho", "Liberia", "Malawi", "Mali", "Mauritania", "Mozambique", "Namibia", "Niger", "Nigeria", "Congo", "Senegal", "South Africa", "Swaziland", "Tanzania", "Togo", "Uganda", "Zambia", "Zimbabwe"])
    },
    13: {
        "member": "bus 03",
        "region": "Atlantic North",
        "coordinates": (-45, 62),
        "countries": ["Greenland", "Iceland"]
    }
}

# Dictionary to store information about the links 
links_dic = {
    "1_2": {
        "name": "North America to Latin America",
        "bus0": (1, "North America"),
        "bus1": (2, "Latin America"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "1_10": {
        "name": "North America to UPS",
        "bus0": (1, "North America"),
        "bus1": (10, "UPS"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "1_13": {
        "name": "North America to Atlantic North",
        "bus0": (1, "North America"),
        "bus1": (13, "Atlantic North"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "3_5": {
        "name": "Oceania to South Asia",
        "bus0": (3, "Oceania"),
        "bus1": (5, "South Asia"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "4_5": {
        "name": "North Asia to South Asia",
        "bus0": (4, "North Asia"),
        "bus1": (5, "South Asia"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "4_6": {
        "name": "North Asia to North West Asia",
        "bus0": (4, "North Asia"),
        "bus1": (6, "North West Asia"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "4_7": {
        "name": "North Asia to South West Asia",
        "bus0": (4, "North Asia"),
        "bus1": (7, "South West Asia"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "4_10": {
        "name": "North Asia to UPS",
        "bus0": (4, "North Asia"),
        "bus1": (10, "UPS"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "6_7": {
        "name": "North West Asia to South West Asia",
        "bus0": (6, "North West Asia"),
        "bus1": (7, "South West Asia"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "6_8": {
        "name": "North West Asia to Middle East",
        "bus0": (6, "North West Asia"),
        "bus1": (8, "Middle East"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "6_10": {
        "name": "North West Asia to UPS",
        "bus0": (6, "North West Asia"),
        "bus1": (10, "UPS"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "8_9": {
        "name": "Middle East to Europe",
        "bus0": (8, "Middle East"),
        "bus1": (9, "Europe"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "8_10": {
        "name": "Middle East to UPS",
        "bus0": (8, "Middle East"),
        "bus1": (10, "UPS"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "8_11": {
        "name": "Middle East to North Africa",
        "bus0": (8, "Middle East"),
        "bus1": (11, "North Africa"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "8_12": {
        "name": "Middle East to Africa",
        "bus0": (8, "Middle East"),
        "bus1": (12, "Africa"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "9_10": {
        "name": "Europe to UPS",
        "bus0": (9, "Europe"),
        "bus1": (10, "UPS"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "9_11": {
        "name": "Europe to North Africa",
        "bus0": (9, "Europe"),
        "bus1": (11, "North Africa"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "9_13": {
        "name": "Europe to Atlantic North",
        "bus0": (9, "Europe"),
        "bus1": (13, "Atlantic North"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    },
    "11_12": {
        "name": "North Africa to Africa",
        "bus0": (11, "North Africa"),
        "bus1": (12, "Africa"),
        "length": None,  # distance between bus 0 and bus 1
        "type": "OH",  # Overhead (OH) or subsea (S)
        "efficiency": 0.0  # Efficiency of the interconnector
    }
}

res_potential_dic = {}
demand_profile_dic ={}
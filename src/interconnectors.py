from pyproj import Geod
from regiondefinitions import regions_dic
def calculate_flows(regions_dic, links_dic, globalgrid):
    for region_key, region_value in regions_dic.items():
        inflow = 0
        outflow = 0
        for link_key, link_value in links_dic.items():
            if region_value["bus"] == link_value["bus0"][0]:
                p0 = globalgrid.links_t.p0[link_value["name"]]
                if p0 > 0:
                    outflow += p0
                elif p0 < 0:
                    inflow += abs(p0)
        region_value["inflow"] = inflow
        region_value["outflow"] = outflow
        region_value["netflow"] = inflow - outflow

    return regions_dic

def efficiency_link(P, V, rho, l):
    """Calculates the relative losses of each interconnector.

    Args:
        P (float): Power capacity of cable in MW
        V (float): Cable volatge in kV 
        rho (float): Resisitivity of cable in ohms/km
        l (float): length of cable in km

    Returns:
        float: Efficiency of the cable 
    """
    I = P / V * 1000 # Current in amperes (A)
    R = rho * l # Resistance in ohms 
    losses = I**2 * R * 1e-6 # total losses in MW
    efficiency =  1 - losses / P # Efficiency of the cable

    return efficiency

def calculate_distance(bus0, bus1):
    """Calculates the actual distance between two points on the earth.

    Args:
        node1 (int): Identifier of bus 0
        node2 (int): Identifier of bus 1

    Returns:
        float: Distance between the two nodes in km.
    """
    geod = Geod(ellps="WGS84")
    lon1, lat1 = regions_dic[bus0]["coordinates"]
    lon2, lat2 = regions_dic[bus1]["coordinates"]
    _, _, distance = geod.inv(lon1, lat1, lon2, lat2)
    return distance / 1000

import json
from shapely.geometry import Polygon
import geopandas as gpd
import pandas as pd

#  [{"lat":-15.87456,"lng":-48.27844}]
def bounds_to_polygon(bounds_str):
    bounds = json.loads(bounds_str)
    coords = []
    for coord in bounds:
        coords.append((coord.get('lat'), coord.get('lng')))
    
    return Polygon(coords)


def bound_series_to_geoseries(bound_series):
    pols = []
    
    for bounds_str in bound_series:
        pols.append(bounds_to_polygon(bounds_str))
        
    return gpd.GeoSeries(pols)

## Polygon -> Bounds

def polygon_to_bound_str(polygon):
    
    def get_bigger_polygon(multi_polygon):
        polys = list(multi_polygon)
        bigger_pol_index = gpd.GeoSeries(list(polys)).area.sort_values(ascending=False).index[0]
        return polys[bigger_pol_index]

    if polygon.type == 'MultiPolygon':
        polygon = get_bigger_polygon(polygon)
        
    lat, long = polygon.exterior.coords.xy        
    
    return pd.DataFrame({'lat': lat, 'lng': long}).to_json(orient='records')

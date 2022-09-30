import osmnx as ox
import geopandas as gpd

place_name = "A Coruña, Galicia, España"
area = ox.geocode_to_gdf(place_name)

tags = {'public_transport': 'platform', 'bus': 'yes'}
stops = ox.geometries_from_place(place_name, tags)
stops.head()
stops.to_file('stops-routes.geosjon', driver='GeoJSON')
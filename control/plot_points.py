from gmplot import gmplot
import geopy # could replace this with some standard ROS package, (maybe hector_geotiff?)
import geopy.distance
import numpy as np

NUM = 1000

# Define starting point.
origin = geopy.Point(37.331553, -121.882767)
# Define azimuth
SPACE_AZIMUTH = -32

def translate_point(origin, dx, dy): # dx, dy in meters

    dist_x = geopy.distance.geodesic(meters = dx)
    dist_y = geopy.distance.geodesic(meters = dy)
    # move by y
    left_upper = dist_y.destination(point=origin, bearing=SPACE_AZIMUTH)
    # move by x
    dest = dist_x.destination(point=left_upper, bearing=SPACE_AZIMUTH+90)
    return dest

# generate 30 points on campus (the dimensions of campus are 650 x 550m)
points_metric = np.hstack([np.random.rand(NUM,1)*650, np.random.rand(NUM,1)*550])

# convert points from metric to (lat,lon,alt) frame
points_geo = np.array([list(translate_point(origin, dx, dy)) for (dx, dy) in points_metric])

# Place map
gmap = gmplot.GoogleMapPlotter(37.335404, -121.883990, 13)

# Scatter points
top_attraction_lats, top_attraction_lons = points_geo[:,0], points_geo[:,1]
gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=2, marker=False)

#nowy_point = translate_point(origin, 100, 500)
#gmap.scatter([nowy_point[0], origin[0]], [nowy_point[1], origin[1]], '#3B0B39', size=2, marker=False)

# Marker
hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

# Draw
gmap.draw("my_map.html")
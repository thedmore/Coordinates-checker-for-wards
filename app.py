from flask import Flask, render_template, request
from shapely.wkt import loads
import csv

app = Flask(__name__)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def point_in_polygon(point, polygon):
    num_vertices = len(polygon)
    x, y = point.x, point.y
    inside = False
 
    p1 = polygon[0]
 
    for i in range(1, num_vertices + 1):
        p2 = polygon[i % num_vertices]
 
        if y > min(p1.y, p2.y):
            if y <= max(p1.y, p2.y):
                if x <= max(p1.x, p2.x):
                    x_intersection = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                    if p1.x == p2.x or x <= x_intersection:
                        inside = not inside
 
        p1 = p2
 
    return inside

def validateCoordinates(id_to_search, checkLatitude, checkLongitude, data_set):
    boundaryCoordinates=[]
    with open(data_set, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['id'] == id_to_search:
                wkt = row['WKT']
                polygon = loads(wkt)
                if polygon.geom_type == 'MultiPolygon':
                    for poly in polygon.geoms:
                        for coord in poly.exterior.coords:
                            longitude, latitude, elevation = coord
                            boundaryCoordinates.append(Point(latitude, longitude))
                else:
                    print("Unknown geometry type")
                break
        else:
            return "ID not found in the CSV."

    point = Point(checkLatitude, checkLongitude)
    if point_in_polygon(point, boundaryCoordinates):
        return "Within boundary"
    else:
        return "Not within boundary"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    id_to_search = data['id']
    latitude = float(data['latitude'])
    longitude = float(data['longitude'])
    data_set = 'Datasets.csv'
    result = validateCoordinates(id_to_search, latitude, longitude, data_set)
    return result

if __name__ == '__main__':
    app.run(debug=True)

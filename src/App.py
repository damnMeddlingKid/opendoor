from flask import Flask, request, render_template, Response
from geojson import Feature, Point, FeatureCollection
import Test

"""Simple flask app to display listings on a map
The dwelling type is hardcoded by the coordinates are passed in from the frontend.
"""

app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route("/get_similar", methods=['GET'])
def get_similar():
    """API endpoint to search for similar houses to a given location
    :param lat,lon: Point on the map to search from of the search query
    :return: GeoJSON encoded collection of locations near the query Point
    """
    try:
        lat = float(request.args.get('lat', ''))
        lon = float(request.args.get('lon', ''))
    except:
        print "error"

    house = Test.generate_datum()
    house['lat'] = lat
    house['lon'] = lon
    house['dwelling_type'] = 'single-family'
    houses = house.get_similar(10)

    geo_houses = []

    for i in range(0,10):
        house = houses.iloc[i]
        feature = Feature(geometry=Point((house['lon'],house['lat'])))
        feature['dwelling_type'] = house['dwelling_type']
        feature['pool'] = house['pool']
        feature['list_price'] = house['list_price']
        geo_houses.append(feature)

    return Response(str(FeatureCollection(geo_houses)), mimetype="application/json")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    Test.generate_test_set()
    app.run(debug=True, host='0.0.0.0')

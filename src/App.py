from flask import Flask, request, render_template, Response
from geojson import Feature, Point, FeatureCollection
import Test
from House import House
app = Flask(__name__,template_folder="../templates",static_folder="../static")

@app.route("/get_similar", methods=['GET'])
def get_similar():
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
    app.run(debug=True)

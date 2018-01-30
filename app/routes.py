from app import app
from geopy import geocoders
'''gn = geocoders.GeoNames()'''
import requests
from flask import request
import json
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']

    airquality_url = 'https://api.breezometer.com/baqi/?lat=' + str(lat) + '&lon=' + str(lon) +'&key=74a3fdfe934f4e5c8b0cc50edfb225bd'
    airquality_request = requests.get(airquality_url)
    airquality_json = json.loads(airquality_request.text)

    aqi = (airquality_json['breezometer_aqi'])
    rr = (airquality_json['random_recommendations']['outside'])

    return render_template('index.html', airqualityindex=aqi, rr=rr)

@app.route('/placedetails')
def placedetails():
    zipcode = request.args.get('zipcode')
    print (zipcode)
    # send_url = 'http://freegeoip.net/json'
    google_geocodeurl = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + zipcode
    # r = requests.get(send_url)
    # j = json.loads(r.text)
    # lat = j['latitude']
    # lon = j['longitude']

    zipcoderequest = requests.get(google_geocodeurl)
    zipcodejson = json.loads(zipcoderequest.text)

    zipcodelatitude= zipcodejson['results'][0]['geometry']['location']['lat']
    zipcodelongitude = zipcodejson['results'][0]['geometry']['location']['lng']

    airquality_url = 'https://api.breezometer.com/baqi/?lat=' + str(zipcodelatitude) + '&lon=' + str(zipcodelongitude) +'&key=74a3fdfe934f4e5c8b0cc50edfb225bd'

    airquality_request = requests.get(airquality_url)
    airquality_json = json.loads(airquality_request.text)

    ''' print (airquality_json) '''

    k = (airquality_json['breezometer_description'])
    aqi = (airquality_json['breezometer_aqi'])
    rr = (airquality_json['random_recommendations']['outside'])
    return render_template('index.html', airqualityindex=aqi, rr=rr)

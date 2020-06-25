from flask import Flask, render_template, request, url_for, redirect, message_flashed, flash, jsonify
import requests
import wikipediaapi
import time
import json
import re
from config.config_reader import config_json_read

app = Flask(__name__)

data = config_json_read()

ipstack = data['api_keys']['ipstack']
openweathermap = data['api_keys']['openweathermap']
opentripmap = data['api_keys']['opentripmap']
devhere = data['api_keys']['developerhere']


@app.route('/')
def index():
    if request.method == 'POST':
        city = request.form['city_name']
        return redirect(url_for('search', city=city))

    if request.method == 'GET':

        '''
        Get the IP address of the client
        '''

        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip_add = request.environ['REMOTE_ADDR']
        else:
            ip_add = request.environ['HTTP_X_FORWARDED_FOR']

        '''
        Get the city name from the IP address. The city name variable is placed in ip_city 
        '''
        #Cape Town
        #ip_add = ''

        '''
        Get the city name via the IP address. Send IP address to the IP Stack API
        '''

        get_city_url = 'http://api.ipstack.com/{}?access_key={}'

        ip_r = requests.get(get_city_url.format(ip_add, ipstack))
        ip_d = json.loads(ip_r.text)
        ip_city = ip_d['city']


        if ip_city == None:
            ip_city = ip_d['location']['capital']


        '''
        Get the weather details via the city name. Send the city name to the Open Weather Map API
        '''

        weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}' \
                      '&units=metric&mode=json&APPID={}'

        r = requests.get(weather_url.format(ip_city, openweathermap))
        weather_data = json.loads(r.text)

        try:
            weather_city = weather_data['name']
        except KeyError:
            city = ip_city
            return render_template('error.html', city=city)


        weather = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        sunrise = weather_data['sys']['sunrise']
        sunset = weather_data['sys']['sunset']

        sunrise = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sunrise))
        sunset = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sunset))

        sunset = re.sub(r'^[^ ]*', '', sunset)
        sunrise = re.sub(r'^[^ ]*', '', sunrise)

        '''
        Get the picture via the city name. If the city name matches the list get picture else make city None
        '''

        urban_areas_url = 'http://api.teleport.org/api/urban_areas/'
        r = requests.get(urban_areas_url)
        data = json.loads(r.text)

        city_url = None
        item = data['_links']['ua:item']
        for city in item:
            if city['name'] == ip_city:
                city_url = city['href']

        if city_url != None:

            city_r = requests.get(city_url)
            city_d = json.loads(city_r.text)

            city_item = city_d['_links']['ua:images']['href']

            image_r = requests.get(city_item)
            image_d = json.loads(image_r.text)

            image_url = image_d['photos'][0]['image']['web']

        else:

            image_url = "nopic"

        '''
        Get the population, countery and coordinate information for the city
        '''

        opentrip_url = "https://api.opentripmap.com/0.1/en/places/geoname?name={}" \
                       "&apikey={}"


        r = requests.get(opentrip_url.format(ip_city, opentripmap))
        data = json.loads(r.text)

        try:
            population = data['population']
            country = data['country']
            lon = data['lon']
            lat = data['lat']
        except KeyError:
            population = 'Not Available'
            country = 'Not Available'
            lon = "Not Available"
            lat = "Not Available"

        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(weather_city)
        summary = page_py.summary.split("\n")

    return render_template('index.html', city_name_upper=weather_city.upper(), city_name=weather_city, weather=weather,
                           temp=int(temp), sunrise=sunrise, sunset=sunset, icon=icon, image_url=image_url,
                           population=population, lon=lon, lat=lat, country=country, devhere=devhere, summary=summary)

@app.route('/search', methods=['GET', 'POST'])
def search():
    city = request.args.get('city')

    if request.method == 'POST':
        city = request.form['city_name']
        return redirect(url_for('search', city=city))

    if request.method == 'GET':

        weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}' \
                      '&units=metric&mode=json&APPID={}'
        city_name = city

        r = requests.get(weather_url.format(city_name, openweathermap))
        weather_data = json.loads(r.text)

        try:
            weather_city = weather_data['name']
        except KeyError:
            return render_template('error.html', city=city)

        weather = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        sunrise = weather_data['sys']['sunrise']
        sunset = weather_data['sys']['sunset']

        sunrise = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sunrise))
        sunset = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sunset))

        sunset = re.sub(r'^[^ ]*', '', sunset)
        sunrise = re.sub(r'^[^ ]*', '',  sunrise)

        urban_areas_url = 'http://api.teleport.org/api/urban_areas/'
        r = requests.get(urban_areas_url)
        data = json.loads(r.text)

        city_url = None
        item = data['_links']['ua:item']
        for c in item:
            if c['name'] == city.title():
                city_url = c['href']

        if city_url != None:

            city_r = requests.get(city_url)
            city_d = json.loads(city_r.text)

            city_item = city_d['_links']['ua:images']['href']

            image_r = requests.get(city_item)
            image_d = json.loads(image_r.text)

            image_url = image_d['photos'][0]['image']['web']

        else:

            image_url = "nopic"

        '''
        Get the population and coordinate information for the city
        '''

        opentrip_url = "https://api.opentripmap.com/0.1/en/places/geoname?name={}" \
                       "&apikey={}"


        r = requests.get(opentrip_url.format(city_name, opentripmap))
        data = json.loads(r.text)

        try:
            population = data['population']
            country = data['country']
            lon = data['lon']
            lat = data['lat']
        except KeyError:
            population = 'Not Available'
            country = 'Not Available'
            lon = "Not Available"
            lat = "Not Available"

        #Get WIKI info for City

        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(city)
        summary = page_py.summary.split("\n")

        return render_template('search.html', city_name_upper=weather_city.upper(), city_name=weather_city,
                               weather=weather, temp=int(temp), sunrise=sunrise, sunset=sunset, icon=icon,
                               image_url=image_url, population=population, lon=lon, lat=lat, country=country,
                               devhere=devhere, summary=summary)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5100, debug=True)
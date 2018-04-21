import json, urllib
from google.appengine.api import urlfetch
from models import Settings

def geocode(address):
    key = Settings.get('GOOGLE_MAPS_API_KEY')
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.quote(address) + '&key=' + key
    return json.loads(urlfetch.fetch(url).content)

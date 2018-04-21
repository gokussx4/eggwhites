import json, urllib
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from models import GeoCache, Settings

def geocode(address):
    geo = GeoCache.get_by_address(address)
    if (geo != None):
        return geo.geo
    geo = _request(address)
    if (geo is None):
        return None
    geo.put()
    return geo.geo

def _request(address):
    key = Settings.get('GOOGLE_MAPS_API_KEY')
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.quote(address) + '&key=' + key
    res = json.loads(urlfetch.fetch(url).content)['results']
    if (len(res) == 0):
        return None
    loc = res[0]['geometry']['location']
    geo = ndb.GeoPt(loc['lat'], loc['lng'])
    return GeoCache(address = address, geo = geo)

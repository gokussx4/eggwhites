from google.appengine.ext import ndb
from google.appengine.ext import db
from geo.geomodel import GeoModel

class FastResponder(GeoModel):
    coverage = ndb.IntegerProperty()
    email = ndb.StringProperty()
    location = ndb.GeoPtProperty()
    name = ndb.StringProperty()
    phone = ndb.StringProperty()

def create_entity_using_attributes(coverage, email, location, name, phone):
    fast_responder_instance = FastResponder()
    fast_responder_instance.coverage = coverage
    fast_responder_instance.email = email
    fast_responder_instance.location = location
    fast_responder_instance.name = name
    fast_responder_instance.phone = phone
    return fast_responder_instance

def save_entity(fast_responder_instance):
    fast_responder_instance_key = fast_responder_instance.put()
    return fast_responder_instance_key

def get_entity(fast_responder_instance_key):
    fast_responder_instance = fast_responder_instance_key.get()
    return fast_responder_instance

def delete_entity(fast_responder_instance):
    fast_responder_instance.key.delete()

def _get_latitude(self):
    return self.location.lat if self.location else None

def _set_latitude(self, lat):
    if not self.location:
      self.location = db.GeoPt()
    self.location.lat = lat
  latitude = property(_get_latitude, _set_latitude)

def _get_longitude(self):
    return self.location.lon if self.location else None

def _set_longitude(self, lon):
    if not self.location:
        self.location = db.GeoPt()

    self.location.lon = lon

longitude = property(_get_longitude, _set_longitude)
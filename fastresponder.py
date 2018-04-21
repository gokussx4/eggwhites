from google.appengine.ext import ndb

class FastResponder(ndb.Model):
    coverage = ndb.IntegerProperty()
    email = ndb.StringProperty()
    location = ndb.GeoPtProperty()
    name = ndb.StringProperty()
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    address2 = ndb.StringProperty()
    city = ndb.StringProperty()
    state = ndb.StringProperty()
    zip = ndb.StringProperty()
    phone = ndb.StringProperty()

def create_entity_using_attributes(coverage, email, location, name, address, address2, city, state, zip, phone):
    fast_responder_instance = FastResponder()
    fast_responder_instance.coverage = coverage
    fast_responder_instance.email = email
    fast_responder_instance.location = location
    fast_responder_instance.name = name
    fast_responder_instance.address = address
    fast_responder_instance.address2 = address2
    fast_responder_instance.city = city
    fast_responder_instance.state = state
    fast_responder_instance.zip = zip
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

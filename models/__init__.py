import json, re
from google.appengine.api import datastore_errors
from google.appengine.ext import ndb

class ModelJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if (isinstance(obj, ndb.Model)):
            mobj = obj.to_dict()
            mobj['id'] = '{0:x}'.format(obj.key.id())
            return mobj
        return json.JSONEncoder.default(self, obj)

class ZipProperty(ndb.StringProperty):
    def _validate(self, value):
        if (not isinstance(value, basestring)):
            raise datastore_errors.BadValueError('Invalid zip')
        if (not re.match(r'^\d{5}(?:[-\s]\d{4})?$', value)):
            raise datastore_errors.BadValueError('Invalid zip')

class Settings(ndb.Model):
  name = ndb.StringProperty()
  value = ndb.StringProperty()

  @staticmethod
  def get(name):
    NOT_SET_VALUE = "NOT SET"
    retval = Settings.query(Settings.name == name).get()
    if not retval:
      retval = Settings()
      retval.name = name
      retval.value = NOT_SET_VALUE
      retval.put()
    if retval.value == NOT_SET_VALUE:
      raise Exception(('Setting %s not found in the database.') % (name))
    return retval.value

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    address = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    state = ndb.StringProperty(required=True)
    zip = ZipProperty(required=True)

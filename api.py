import json
import urllib
import webapp2
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

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


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<form method=post><textarea name=address></textarea><br><button type=submit>Search</button></form>')
    def post(self):
        address = self.request.POST['address']
        key = Settings.get('GOOGLE_MAPS_API_KEY')
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.quote(address) + '&key=' + key
        obj = json.loads(urlfetch.fetch(url).content)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(json.dumps(obj['results'][0]['geometry']['location']))

class JsonResponse(webapp2.Response):
    def __init__(self, body, status=200):
        super(webapp2.Response, self).__init__()
        self.status = status
        self.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.body = json.dumps(body) + '\n'

class JsonApi(webapp2.RequestHandler):
    def handle_exception(self, exception, debug_mode):
        status = 500
        body = {'message': 'Internal Server Error'}

        if (isinstance(exception, webapp2.HTTPException)):
            status = exception.code
            body['message'] = exception.title

        return JsonResponse(body, status)

class UserApi(JsonApi):
    def post(self):
        self.abort(501)

app = webapp2.WSGIApplication([
    ('/api/', MainPage),
    ('/api/v0/user', UserApi),
], debug=True)

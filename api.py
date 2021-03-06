import collections
import json
import logging
import numpy as np
from gmaps import geocode
from models import ModelJSONEncoder, User
import urllib
import webapp2
from google.appengine.api import datastore_errors, urlfetch
import distance


class JsonResponse(webapp2.Response):
    def __init__(self, body, status=200):
        super(webapp2.Response, self).__init__()
        self.status = status
        self.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.body = json.dumps(body, cls=ModelJSONEncoder) + '\n'

class JsonApi(webapp2.RequestHandler):
    def get_body(self):
        if (self.request.headers['Content-Type'] != 'application/json'):
            self.abort(400)
        try:
            return json.loads(self.request.body)
        except:
            self.abort(400)
    def put_object(self, Object, data):
        try:
            obj = Object(**data)
            obj.put()
            return obj
        except AttributeError:
            self.abort(400)
        except datastore_errors.BadValueError as ex:
            self.abort(400, title=ex.message)
    def handle_exception(self, exception, debug_mode):
        status = 500
        body = {'message': 'Internal Server Error'}

        if (isinstance(exception, webapp2.HTTPException)):
            status = exception.code
            body['message'] = exception.title
        else:
            logging.exception(exception)

        return JsonResponse(body, status)

class UserBaseApiHandler(JsonApi):
    def post(self):
        data = self.get_body()
        if ('id' in data):
            self.abort(400)
        user = self.put_object(User, data)
        return JsonResponse(user)
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

class UserApiHandler(JsonApi):
    def get(self, user_key):
        user = User.get_by_key(user_key)
        if (user is None):
            self.abort(404)
        return JsonResponse(user)

class UserSearchApiHandler(JsonApi):
    def post(self):
        data = self.get_body()
        geo = geocode(data['address'])
        pos1 = np.array([geo.lat, geo.lon])
        pos2Dictionary = collections.OrderedDict()
        for user in User.query().fetch():
            user_geo = geocode(user.full_address())
            if (user_geo != None):
                pos2Dictionary[user.key.id()] = [user_geo.lat, user_geo.lon]
        dists = distance.get_distance_sorted_responders(pos1, pos2Dictionary)
        user = User.get_by_id(dists.keys()[0])
        return JsonResponse(user)

def handle_404(request, response, exception):
    return JsonResponse({'message': 'Not Found'}, 404)

def handle_405(request, response, exception):
    return JsonResponse({'message': 'Method Not Allowed'}, 405)

app = webapp2.WSGIApplication([
    (r'/api/v0/user', UserBaseApiHandler),
    (r'/api/v0/user/search', UserSearchApiHandler),
    (r'/api/v0/user/([0-9a-zA-Z-]+)', UserApiHandler),
], debug=True)

app.error_handlers[404] = handle_404
app.error_handlers[405] = handle_405

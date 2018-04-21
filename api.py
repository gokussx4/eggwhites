import json
import logging
from gmaps import geocode
from models import ModelJSONEncoder, User
import urllib
import webapp2
from google.appengine.api import datastore_errors, urlfetch


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<form method=post><textarea name=address></textarea><br><button type=submit>Search</button></form>')
    def post(self):
        address = self.request.POST['address']
        obj = geocode(address)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(json.dumps(obj['results'][0]['geometry']['location']))

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
        user = self.put_object(User, data)
        return JsonResponse(user)

class UserApiHandler(JsonApi):
    def get(self, user_id):
        user = User.get_by_id(long(user_id, base=16))
        if (user is None):
            self.abort(404)
        return JsonResponse(user)

def handle_404(request, response, exception):
    return JsonResponse({'message': 'Not Found'}, 404)

app = webapp2.WSGIApplication([
    (r'/api/', MainPage),
    (r'/api/v0/user', UserBaseApiHandler),
    (r'/api/v0/user/([0-9a-f]+)', UserApiHandler),
], debug=True)

app.error_handlers[404] = handle_404

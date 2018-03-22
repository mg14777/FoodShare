import webapp2
import renderView as view
from google.appengine.ext import ndb
import datastore

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        contribution_key = ndb.Key(urlsafe=self.request.get('key'))
        contribution = contribution_key.get()
        if contribution.picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(contribution.picture)
        else:
            self.response.out.write('No image')
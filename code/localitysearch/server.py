import webapp2
from handlers.localitysearch import LocalitySearchHandler
import datastore

class TestHandler(webapp2.RequestHandler):
    def dbtest(self):
        datastore.test_contributions_py()
        self.redirect('/')
    def dbtestprint(self):
        contributions = datastore.get_contributions();
        for contr in contributions:
            print contr.to_dict()
        self.redirect('/')

app = webapp2.WSGIApplication([
    webapp2.Route('/localitysearch',
        handler=LocalitySearchHandler,
        name='get',
        handler_method='localitysearch')
], debug=True)
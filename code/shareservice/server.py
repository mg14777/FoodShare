import webapp2
from handlers.contributions import ContributionHandler
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
    webapp2.Route('/uploadcontribution', 
        handler=ContributionHandler, 
        name='create', 
        handler_method='create'),
    webapp2.Route('/contribution', 
        handler=ContributionHandler, 
        name='get_details', 
        handler_method='get_details'),
    webapp2.Route('/consume', 
        handler=ContributionHandler, 
        name='consume', 
        handler_method='consume')
], debug=True)
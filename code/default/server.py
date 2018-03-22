import webapp2
from handlers.default import DefaultHandler
from handlers.users import UserHandler
from handlers.contributions import ContributionHandler
from handlers.images import ImageHandler
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
    webapp2.Route('/', 
        handler=DefaultHandler, 
        name='homepage', 
        handler_method='homepage'),
    webapp2.Route('/dashboard', 
        handler=DefaultHandler, 
        name='dashboard', 
        handler_method='dashboard'),
    webapp2.Route('/contribute', 
        handler=DefaultHandler, 
        name='contribute', 
        handler_method='contribute'),
    webapp2.Route('/viewcontribution', 
        handler=DefaultHandler, 
        name='view_contribution', 
        handler_method='view_contribution'),

    webapp2.Route('/login', 
        handler=UserHandler, 
        name='login', 
        handler_method='login'),
    webapp2.Route('/logout', 
        handler=UserHandler, 
        name='logout', 
        handler_method='logout'),
    webapp2.Route('/imgsrv', 
        handler=ImageHandler, 
        name='get', 
        handler_method='get'),
    webapp2.Route('/localitysearch',
        handler=LocalitySearchHandler,
        name='get',
        handler_method='localitysearch'),
    webapp2.Route('/updateuserphoto', 
        handler=UserHandler, 
        name='updatePhoto', 
        handler_method='updatePhoto'),
    webapp2.Route('/updateuserreputation', 
        handler=UserHandler, 
        name='updateReputation', 
        handler_method='updateReputation'),
    



    webapp2.Route('/dbtest', 
        handler=TestHandler, 
        name='dbtest', 
        handler_method='dbtest'),
    webapp2.Route('/dbtestprint', 
        handler=TestHandler, 
        name='dbtestprint', 
        handler_method='dbtestprint')
], debug=True)
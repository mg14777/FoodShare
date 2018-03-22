import webapp2
import renderView as view
from google.appengine.api import users
from google.appengine.api import urlfetch
import datastore as ds
import json

class DefaultHandler(webapp2.RequestHandler):
    def homepage(self):

        page_data = ds.Contribution.get20FullList()
        user = users.get_current_user()
        user_dict = dict()
        if user:
            user_dict = {
                'name': user.nickname()
            }
        self.response.write(view.renderHome('home-page', page_data, user_dict))

    def dashboard(self):
        user = users.get_current_user()
        if user:
            user_dict = {
                'name': user.nickname()
            }    
        else:  
            self.redirect('/login')    

        page_data = {}
        page_data['active_contributions'] = ds.Contribution.getUserActiveContributionsDict(user.user_id())
        page_data['consumed_contributions'] = ds.Consumption.getUserConsumedContributionsDict(user.user_id())
        page_data['consumptions'] =  ds.Consumption.getUserConsumptionsDict(user.user_id())

        self.response.write(view.renderGeneric('dashboard', page_data, user_dict))

    def contribute(self):
        page_data = []
        self.response.write(view.render('contribute-form', page_data))

    def view_contribution(self):
        if 'key' in self.request.GET:
            url_key = self.request.GET['key']
            fetch_url = self.request.host_url + "/contribution?key="+url_key
            try:
                result = urlfetch.fetch(fetch_url)
                page_data = json.loads(result.content)

                if result.status_code == 200:
                    user = users.get_current_user()
                    user_dict = dict()
                    if user:
                        user_dict = {
                            'name': user.nickname()
                        }
                    self.response.write(view.renderContribution('contribution', page_data, user_dict))  
                else:
                    self.response.status_code = result.status_code
            except urlfetch.Error:
                self.response.write("No contribution id specified")

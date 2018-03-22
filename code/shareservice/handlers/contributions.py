import webapp2
import logging
from google.appengine.api import users
import datastore as ds
from google.appengine.ext import ndb
import json

class ContributionHandler(webapp2.RequestHandler):
    def create(self):
        user = users.get_current_user()
        if user:
            contribution = dict()
            contribution['contributor_id'] = user.user_id()
            contribution['contributor'] = user.nickname()
            contribution['food_name'] = self.request.get('food')
            contribution['picture'] = self.request.get('pic')
            contribution['expiry_delta'] = self.request.get('expiry')
            contribution['description'] = self.request.get('description')
            contribution['address'] = self.request.get('address')
            contribution['city'] = self.request.get('city')
            contribution['country'] = self.request.get('country')
            contribution['postcode'] = self.request.get('postcode')
            success = ds.Contribution.validate_and_add_contribution(contribution, user.email())

            self.response.write(success)
        else: 
            self.response.write("error")

    def get_details(self):
        if 'key' in self.request.GET:
            url_key = self.request.GET['key']
            key = ndb.Key(urlsafe=url_key)
            contribution = key.get()
            page_data = ds.Contribution.convertDictFull(contribution)
            page_data['picture'] = ""
            page_data['timestamp'] = page_data['timestamp'].isoformat()
            page_data['expiry'] = page_data['expiry'].isoformat()
            self.response.write(json.dumps(page_data))
        else:
            self.response.write("Error")

    def consume(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')

        if 'key' in self.request.GET:
            url_key = self.request.GET['key']
            ds.Consumption.addConsumption(url_key, user.user_id())


        self.redirect('/')




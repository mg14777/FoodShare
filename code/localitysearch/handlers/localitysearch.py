import webapp2
import logging
import datastore as ds
import googlemaps
import json

class LocalitySearchHandler(webapp2.RequestHandler):

	def localitysearch(self):
		user_lat = self.request.get('lat')
		user_lng = self.request.get('lng')
		gmaps = googlemaps.Client(key='AIzaSyCyRggT3qkX354uU6cxeTbe-A7iOfgacbk')
		user_address = gmaps.reverse_geocode((user_lat,user_lng))[0]
		user_address = user_address['address_components']
		user_city = ''
		#city_contributions = ds.getContributionsInCity()
		for component in user_address:
			if 'locality' in component['types']:
				user_city = component['short_name']
		user_city_contributions = ds.Contribution.getContributionsInCity(user_city)
		user_city_contributions_addresses = []
		for user_city_contribution in user_city_contributions:
			user_city_contributions_addresses.append(user_city_contribution['address']+", "+user_city_contribution['city']+", "+user_city_contribution['country']+", "+user_city_contribution['postcode'])
		nearby_coords = []
		for user_city_contributions_address in user_city_contributions_addresses:
			geocode_response = gmaps.geocode(user_city_contributions_address)[0]
			nearby_coords.append(geocode_response['geometry']['location'])
		return self.response.write(json.dumps(nearby_coords))
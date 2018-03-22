import webapp2
import logging
from google.appengine.api import users

class UserHandler(webapp2.RequestHandler):
	def login(self):
		redirect_url = self.request.host_url + '/'
		if 'redirect_url' in self.request.GET:
			redirect_url += self.request.GET['redirect_url']
		self.redirect(users.create_login_url(redirect_url))
	def logout(self):
		redirect_url = self.request.host_url + '/'
		if 'redirect_url' == self.request.GET:
			redirect_url += self.request.GET['redirect_url']
		self.redirect(users.create_logout_url(redirect_url))
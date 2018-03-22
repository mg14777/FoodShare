import jinja2
import os

# Initialise jinja2 templating environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def render(template_url, data):
		template_url = 'templates/' + template_url + '.html'
		template = JINJA_ENVIRONMENT.get_template(template_url)
		return template.render(data)

def renderHome(template_url, data, user):
		template_url = 'templates/' + template_url + '.html'
		template = JINJA_ENVIRONMENT.get_template(template_url)
		return template.render(topContributions=data, user=user)

def renderContribution(template_url, data, user):
		template_url = 'templates/' + template_url + '.html'
		template = JINJA_ENVIRONMENT.get_template(template_url)
		return template.render(contribution=data, user=user)

def renderGeneric(template_url, data, user, update=None):
	template_url = 'templates/' + template_url + '.html'
	template = JINJA_ENVIRONMENT.get_template(template_url)
	return template.render(page_data=data, user=user, update=update)
from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.api import users

def sendMail(subject="", body="", user_email = None): 
    if not user_email:
        user_email = users.get_current_user().email()   

    sender_address =  "ionescu.calin.m@gmail.com" #'{}@appspot.gserviceaccount.com'.format(app_identity.get_application_id())
    mail.send_mail(sender=sender_address,
                   to=user_email,
                   subject=subject,
                   body=body)

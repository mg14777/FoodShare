from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
import datetime
import time
import copy
import mailsender as ms

class Food(ndb.Model):
    food = ndb.StringProperty()
    #name, should be unique

    @classmethod
    def get_name(cls, idx):
        #get name by id
        return cls.get_by_id(idx).food

    # TODO: change to strict consistency (use ancestor)
    @classmethod
    def add_entry(cls, food):
        #check if name exists
        item = cls.query(Food.food==food)
        if item.get():
            print "Food item already exists"
            return item.get().key.id()
        else: 
            item = Food(food=food)
            item.put()
            return item.key.id()


class Share(polymodel.PolyModel):
    contributor_id = ndb.StringProperty()
    contributor_email = ndb.StringProperty()
    contributor = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    expiry = ndb.DateTimeProperty(auto_now_add=True)
    description = ndb.StringProperty()
    food_id = ndb.IntegerProperty()
    address = ndb.StringProperty()
    city = ndb.StringProperty()
    country = ndb.StringProperty()
    postcode = ndb.StringProperty()
    picture = ndb.BlobProperty()
    available = ndb.BooleanProperty()

    @classmethod
    def add_contribution(cls, contributor_id, contributor, expiry_delta, description, food_name, picture, address, city, country, postcode, contributor_email, timestamp = None):
        if not timestamp:
            timestamp = datetime.datetime.now()
        expiry = timestamp + datetime.timedelta(int(expiry_delta))

        food_id = Food.add_entry(food_name)
        contr = cls(contributor_id=contributor_id,
            contributor=contributor, food_id=food_id,
            timestamp=timestamp, expiry=expiry, 
            description=description, available=True, picture=picture,
            address=address, city=city, country=country, postcode=postcode, contributor_email=contributor_email)
        future = contr.put()
        #return future.check_success()

    @classmethod 
    # From dict constructor, validates input
    def validate_and_add_contribution(cls, c, contributor_email=""):
        food_name = c['food_name']
        pic = c['picture']
        c_id = c['contributor_id']
        if food_name and pic and c_id :
            expiry_delta = c['expiry_delta']
            #location = c['location']
            address = c['address']
            city = c['city']
            country = c['country']
            postcode = c['postcode']
            c_name = c['contributor']
            if not c_name:
                c_name = 'Anonymous'
            if not expiry_delta:
                expiry_delta = 24
            description = c['description']

            contr_key = cls.add_contribution(c_id, c_name, expiry_delta, description, food_name, pic, address, city, country, postcode, contributor_email)

            subject = "Created contribution "
            body = ""
            ms.sendMail(subject=subject, body=body)

            return contr_key
        else:
            return False

    @classmethod
    def convertQueryToDict(cls, contributions):
        result = []
        if contributions:
            for contr in contributions:
                result.append(cls.convertDictFull(contr))
        return result  

    @classmethod
    def get20(cls):
        # anc = Contribution(contributor_id="")
        return cls.query().fetch(20)
    
    @classmethod 
    def convertDictFull(cls, contribution):
        data = None
        if contribution:
            data = copy.copy(contribution.to_dict())
            data['key'] = contribution.key.urlsafe()
            data['food'] = Food.get_name(contribution.food_id)
        return data

    @classmethod
    def get20FullList(cls):
        contributions = cls.get20()
        return cls.convertQueryToDict(contributions)



########### CONTRIBUTONS ##########

class Contribution(Share):
    @classmethod 
    def getUserActiveContributionsDict(cls, user_id):
        contributions = cls.getUserActiveContributions(user_id)
        return cls.convertQueryToDict(contributions)

    @classmethod
    def getUserActiveContributions(cls, user_id):
    	anc = Contribution(contributor_id=user_id)
        return cls.query(cls.contributor_id==user_id, ancestor=anc.key).fetch()

    @classmethod
    def getContributionsInCity(cls, city):
        allContributions = cls.query(cls.city==city)
        return cls.convertQueryToDict(allContributions)

######  CONSUMPTIONS #######
class Consumption(Share):
    consumer_id = ndb.StringProperty()
    consumption_date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod 
    def getUserConsumedContributionsDict(cls, user_id):
        contributions = cls.getUserConsumedContributions(user_id)
        return cls.convertQueryToDict(contributions)

    @classmethod
    def getUserConsumedContributions(cls, user_id):
        anc = Consumption(contributor_id=user_id)
        return cls.query(cls.contributor_id==user_id, ancestor=anc.key).fetch()

    @classmethod
    def addConsumptionFromContribution(cls, c, c_id):
        cons = Consumption(contributor_id=c.contributor_id, 
            contributor=c.contributor, timestamp=c.timestamp,
            expiry=c.expiry, description=c.description,
            food_id=c.food_id, location=c.location, 
            picture=c.picture, consumer_id=c_id)
       	cons.put()
    @classmethod
    def addConsumption(cls, key_string, consumer_id):
        contr_key = ndb.Key(urlsafe=key_string)
        contr = contr_key.get()
        if contr:
            contr_key.delete()
            cls.addConsumptionFromContribution(contr, consumer_id)

            subject = "Consumed contribution "
            body = ""
            ms.sendMail(subject=subject, body=body)
            subject = "Someone consumed one of your contributions. Hurray"
            ms.sendMail(subject=subject, body=body, user_email=contr.contributor_email)
            return True
        else:
            return False

    @classmethod 
    def getUserConsumptionsDict(cls, user_id):
        consumptions = cls.query(cls.consumer_id == user_id).fetch()
        return cls.convertQueryToDict(consumptions)


class UserWrapper(ndb.Model):
    user_id = ndb.IntegerProperty()
    user_picture = ndb.BlobProperty()
    # user_location = ndb.BlobProperty()
    limit = ndb.IntegerProperty() #Limit how many items an user can take
    reputation = ndb.IntegerProperty()

    @classmethod 
    def getUser(cls, user_id):
        user = cls.query(cls.user_id==user_id).get()
        if user:
            return user
        else:
            user = UserWrapper(user_id=user_id, user_picture=None,
                limit=10, reputation=5)
            user_key = user.put()
            return user_key.get()


    @classmethod 
    def updatePhoto(cls, user_id, picture):
        user = cls.getUser()
        user.picture = picture
        user.put()

    @classmethod
    def updateReputation(cls, user_id, reputation):
        user = cls.getUser()
        user.reputation = reputation
        user.put()




##### TESTING ####
def add_test_contribution(contributor_id, contributor, food_name):
    expiry = datetime.datetime.now()
    expiry += datetime.timedelta(hours=23,minutes=59)
    
    food_id = Food.add_entry(food_name)
    contr = Contribution(
        contributor_id=contributor_id, contributor=contributor,
        expiry=expiry, description='Amazing free food, 100 safe',
        available=True, food_id=food_id)
    future = contr.put()
    # return future.check_success()

def add_test_consumption(contributor_id, contributor, food_name):
    expiry = datetime.datetime.now()
    expiry += datetime.timedelta(hours=23,minutes=59)
    
    food_id = Food.add_entry(food_name)
    contr = Consumption(
        contributor_id=contributor_id, contributor=contributor,
        expiry=expiry, description='Amazing free food, 100 safe',
        available=True, food_id=food_id)
    future = contr.put()

def get_contributions():
    contributions = Contribution.get20()
    return contributions


def test_contributions_py():
    add_test_contribution(6, 'Sandy', 'banana')
    add_test_consumption(6, 'Sandy', 'banana')
    add_test_consumption(2, 'Sandy', 'banana')
    # time.sleep(0.5)
    add_test_contribution(6, 'Sandy', 'banana')
    # time.sleep(0.5)
    add_test_contribution(1, 'Randy', 'banana')
    # time.sleep(0.5)
    add_test_contribution(2, 'Mandy', 'banana')
    # time.sleep(0.5)
    add_test_contribution(3, 'Brandy', 'banana')
    # time.sleep(0.5)
    add_test_contribution(4, 'Andy', 'banana')
    # time.sleep(0.5)
    add_test_contribution(5, 'Lundy', 'banana')


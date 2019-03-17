from . import db
from werkzeug.security import generate_password_hash

import datetime


class UserProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'user_profiles'

    userid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    gender = db.Column(db.String(255))
    email = db.Column(db.String(80), unique=True)
    location = db.Column(db.String(255))
    biography = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    created_on = db.Column(db.String(80))


    
    def __init__(self, first_name, last_name, gender, email, location, biography, photo):
        self.firstname = first_name
        self.lastname = last_name
        self.gender = gender
        self.email = email
        self.location = location
        self.biography = biography
        self.photo = photo
        joined = datetime.datetime.today()
        self.created_on = joined.strftime("%B %d, %Y")  
         


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.userid)  # python 2 support
        except NameError:
            return str(self.userid)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.firstname)
        

        

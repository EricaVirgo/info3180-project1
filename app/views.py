"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""


from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import NewProfileForm
from app.models import UserProfile
from werkzeug.utils import secure_filename
#from werkzeug.security import check_password_hash 
#from werkzeug.security import generate_password_hash

import os
import datetime

def format_date_joined(y, m, d):
    date_joined = datetime.date(y, m, d) 
    return date_joined.strftime("%B %d, %Y")


def get_uploaded_images():
    photo_list = []
    rootdir = os.getcwd()
    for subdir, dir, files in os.walk(rootdir + '/app/static/uploads'):
        for file in files:
            photo_list = photo_list + [os.path.join(file)]
    return photo_list 

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/profile/', methods=["POST", "GET"])
def profile():
    """Render the website's add new profile page."""
    NewP = NewProfileForm()
    
    now = datetime.datetime.today()

    if request.method =="POST":

        if NewP.validate_on_submit():
            #collects user information
            fname = NewP.firstname.data
            lname = NewP.lastname.data
            email = NewP.email.data
            loc = NewP.location.data
            gender = NewP.gender.data
            biography = NewP.biography.data
            
            #saves the photo
            photo = request.files['photo']
            filename = secure_filename(photo.filename)
            photo.save(os.path.join( app.config['UPLOAD_FOLDER'], filename))
    
            #generates the created_on date
            created_on=format_date_joined(now.year, now.month,now.day)
            
            
            new_Prof = UserProfile(first_name=fname, last_name=lname, gender=gender, email=email, location=loc, biography=biography, photo=filename, joined=created_on)
            
            db.session.add(new_Prof)
            db.session.commit()
            
            flash("Profile added.", "success")
            return redirect(url_for("profiles")  )          
            
        else:
            flash("Incorrect information submitted.", "danger")
            return redirect(url_for("profile"))
        
    return render_template('profile.html', form=NewP )

@app.route('/profiles/')
def profiles():
    """Render the website's list of profiles page."""
    profs = UserProfile.query.order_by(UserProfile.lastname).all()
    return render_template('profiles.html', users=profs)

@app.route('/profile/<userid>', methods=["GET"])
def viewProfile(userid):
    """Render the website's individual profile page by specific user id."""
    profile = UserProfile.query.filter_by(ID=userid).first()
    return render_template('profiles.html', users=profile )




###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")

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
from werkzeug.security import check_password_hash 
from werkzeug.security import generate_password_hash

import datetime

def format_date_joined(y, m, d):
    date_joined = datetime.date(y, m, d) 
    return date_joined.strftime("%B %d, %Y")



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
            
            flash("Profile added.", "success")
            return redirect(url_for("profiles")  )          
            
        else:
            flash("Incorrect information submitted.", "danger")
            return redirect(url_for("profile"))
        
    return render_template('profile.html', form=NewP, created_on=format_date_joined(now.year, now.month,now.day) )

@app.route('/profiles/')
def profiles():
    """Render the website's list of profiles page."""
    return render_template('profiles.html')

@app.route('/profile/<userid>')
def viewProfile():
    """Render the website's individual profile page by specific user id."""
    return render_template('about.html')




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

# Reused g+ and fb login/logout code from
# restaurant menu app built in fsf course

from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Place, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Super Rad Places"


# Connect to Database and create database session
engine = create_engine('sqlite:///placesandusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Main page, shows all categories
@app.route('/')
@app.route('/category')
def mainPage():
    ''' Renders main page, no input necessary for GET '''
    logged_in = False
    categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return render_template('publiccategories.html', categories=categories,
                               logged_in=logged_in)
    else:
        return render_template('categories.html', categories=categories,
                               logged_in=True,
                               logged_in_user_id=login_session['user_id'])


@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    ''' Renders new category page, no input necessary for GET '''
    logged_in = False
    if 'username' not in login_session:
        return redirect('/login')
    else:
        logged_in = True
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('mainPage'))
    else:
        return render_template('newcategory.html', logged_in=logged_in)


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    ''' Renders edit category page, takes category id from url for GET '''
    categoryToEdit = session.query(Category).filter_by(id=category_id).one()
    logged_in = False
    creator_id = categoryToEdit.user_id

    if 'username' in login_session:
        logged_in = True
    else:
        return redirect('/login')
    if request.method == 'POST' and creator_id == login_session['user_id']:
        categoryToEdit.name = request.form['name']
        session.commit()
        return redirect(url_for('mainPage'))
    if creator_id != login_session['user_id']:
        return render_template('unauth.html', logged_in=logged_in)
    else:
        return render_template("editcategory.html", logged_in=logged_in,
                               category=categoryToEdit)


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    ''' Renders delete category page, takes category id from url for GET '''
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    places = session.query(Place).filter_by(category_id=category_id).all()
    logged_in = False
    creator_id = categoryToDelete.user_id

    if 'username' in login_session:
        logged_in = True
    else:
        return redirect('/login')
    if request.method == 'POST' and creator_id == login_session['user_id']:
        if request.form['deleteConfirm'] == "CONFIRM":
            if places:
                for place in places:
                    session.delete(place)
            session.delete(categoryToDelete)
            session.commit()
            return redirect(url_for('mainPage'))
        else:
            return render_template("deletefailed.html", logged_in=logged_in)
    if creator_id != login_session['user_id']:
        return render_template('unauth.html', logged_in=logged_in)
    else:
        return render_template("deletecategory.html", logged_in=logged_in,
                               category=categoryToDelete)


@app.route('/category/<int:category_id>')
@app.route('/category/<int:category_id>/places')
def categoryPage(category_id):
    ''' Renders the category page which lists its contents (places),
        takes category id from url for GET '''
    category = session.query(Category).filter_by(id=category_id).one()
    places = session.query(Place).filter_by(category_id=category_id).all()
    creator = getUserInfo(category.user_id)
    logged_in = False
    if 'username' in login_session:
        logged_in = True
    if logged_in is False or creator.id != login_session['user_id']:
        return render_template('publiccategory.html', category=category,
                               places=places, logged_in=logged_in)
    else:
        return render_template('category.html', category=category,
                               places=places, logged_in=logged_in,
                               logged_in_user_id=login_session['user_id'])


@app.route('/category/<int:category_id>/places/new', methods=['GET', 'POST'])
def newPlace(category_id):
    ''' Renders page to add new place to specific category,
        take category id for GET '''
    category = session.query(Category).filter_by(id=category_id).one()
    cat_creator_id = category.user_id
    logged_in = False
    if 'username' not in login_session:
        return redirect('/login')
    else:
        logged_in = True
    if (request.method == 'POST' and
       cat_creator_id == login_session['user_id']):
            newPlace = Place(
                name=request.form['name'], user_id=login_session['user_id'],
                description=request.form['description'], category=category,
                city=request.form['city'], country=request.form['country'])
            session.add(newPlace)
            session.commit()
            return redirect(url_for('categoryPage', category_id=category.id))
    elif cat_creator_id != login_session['user_id']:
        return render_template("unauth.html", logged_in=logged_in)
    else:
        return render_template('newplace.html', logged_in=logged_in)


@app.route('/category/<int:category_id>/places/<int:place_id>/edit',
           methods=['GET', 'POST'])
def editPlace(category_id, place_id):
    ''' Renders page to edit existing place,
        takes category and place id for GET '''
    category = session.query(Category).filter_by(id=category_id).one()
    placeToEdit = session.query(Place).filter_by(id=place_id).one()
    logged_in = False
    creator_id = placeToEdit.user_id

    if 'username' in login_session:
        logged_in = True
    else:
        return redirect('/login')
    if request.method == 'POST' and creator_id == login_session['user_id']:
        placeToEdit.name = request.form['name']
        placeToEdit.city = request.form['city']
        placeToEdit.country = request.form['country']
        placeToEdit.description = request.form['description']
        session.commit()
        return redirect(url_for('placePage', category_id=category.id,
                                place_id=placeToEdit.id))
    elif creator_id != login_session['user_id']:
        return render_template('unauth.html', logged_in=logged_in)
    else:
        return render_template("editplace.html", logged_in=logged_in,
                               place=placeToEdit)


@app.route('/category/<int:category_id>/places/<int:place_id>/delete',
           methods=['GET', 'POST'])
def deletePlace(category_id, place_id):
    ''' Renders page to delete existing place,
        takes category and place id for GET '''
    category = session.query(Category).filter_by(id=category_id).one()
    placeToDelete = session.query(Place).filter_by(id=place_id).one()
    logged_in = False

    if 'username' in login_session:
        logged_in = True
    else:
        return redirect('/login')
    if (request.method == 'POST' and
       placeToDelete.user_id == login_session['user_id']):
        if request.form['deleteConfirm'] == "CONFIRM":
            session.delete(placeToDelete)
            session.commit()
            return redirect(url_for('categoryPage', category_id=category.id))
        else:
            return render_template("deletefailed.html", logged_in=logged_in)
    if placeToDelete.user_id != login_session['user_id']:
        return render_template('unauth.html', logged_in=logged_in)
    else:
        return render_template("deleteplace.html", logged_in=logged_in,
                               place=placeToDelete)


@app.route('/category/<int:category_id>/places/<int:place_id>')
def placePage(category_id, place_id):
    ''' Renders individual page for place,
        takes category and place id for GET '''
    category = session.query(Category).filter_by(id=category_id).one()
    place = session.query(Place).filter_by(id=place_id).one()
    creator = getUserInfo(place.user_id)
    logged_in = False
    if 'username' in login_session:
        logged_in = True
    if logged_in is False or creator.id != login_session['user_id']:
        return render_template('publicplace.html', category=category,
                               place=place, logged_in=logged_in)
    else:
        return render_template('place.html', category=category, place=place,
                               logged_in=logged_in)


@app.route('/category/JSON')
def categoriesJSON():
    ''' Returns JSON of all categories, no input necessary for GET '''
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


# JSON APIs
@app.route('/category/<int:category_id>/places/JSON')
def categoryJSON(category_id):
    ''' Returns JSON of all places within a category,
        takes category ID for GET '''
    category = session.query(Category).filter_by(id=category_id).one()
    places = session.query(Place).filter_by(
        category_id=category_id).all()
    return jsonify(places=[p.serialize for p in places])


@app.route('/category/<int:category_id>/places/<int:place_id>/JSON')
def placeJSON(category_id, place_id):
    ''' Returns JSON of individual place details,
        takes category and place id for GET '''
    place = session.query(Place).filter_by(id=place_id).one()
    return jsonify(place=place.serialize)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    ''' Renders login page, no input necessary for GET '''
    logged_in = False
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, logged_in=logged_in)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    ''' FB oauth implementation '''
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = '''https://graph.facebook.com/oauth/access_token?
             grant_type=fb_exchange_token&client_id=%s&client_secret=
             %s&fb_exchange_token=%s''' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    # let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = '''https://graph.facebook.com/v2.4/me/picture?%s
             &redirect=0&height=200&width=200''' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
                -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''

    return output


@app.route('/gconnect', methods=['POST'])
def gconnect():
    ''' Google oauth implementation '''
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('''
                                 Current user is already connected.'''), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
                -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    ''' Log out of Google oauth '''
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = '''https://accounts.google.com
             /o/oauth2/revoke?token=%s''' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbdisconnect')
def fbdisconnect():
    ''' Logout of FB oauth '''
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = '''https://graph.facebook.com
             /%s/permissions?access_token=%s''' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    ''' Initiates logout whether user used FB or Google oauth '''
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['state']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']

        return redirect(url_for('mainPage'))
    else:

        return redirect(url_for('mainPage'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = False
    app.run(host='0.0.0.0', port=5000)

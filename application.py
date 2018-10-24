from flask import Flask, render_template, request, redirect, jsonify, url_for, flash  # noqa
from sqlalchemy import create_engine, asc, func
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import urllib
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Video Games Category Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///category_item_user.db?check_same_thread=False')  # noqa
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)  # noqa
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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '  # noqa
    flash("you are now logged in as %s" % login_session['username'])  # noqa
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])  # noqa
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
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))  # noqa
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Category Information
@app.route('/catalog.json')
def CategorysItemsJSON():
    categories = (session.query(Category).all())
    items = (session.query(CategoryItem).filter_by(
        games_category_id=Category.id).all())
    return jsonify(Category=[r.serialize for r in categories], Item=[i.serialize for i in items])  # noqa


# Show all Categorys
@app.route('/')
@app.route('/catalog/')
def showCategorys():
    Categorys = session.query(Category).order_by(asc(Category.name))
    items = session.query(CategoryItem)
    return render_template('Categorys.html', Categorys=Categorys, items=items)  # noqa

# Create a new Category


@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategorys'))
    else:
        return render_template('newCategory.html')

# Edit a Category


@app.route('/catalog/<string:games_name>/<int:games_category_id>/edit/', methods=['GET', 'POST'])  # noqa
def editCategory(games_name, games_category_id):
    editedCategory = session.query(
        Category).filter_by(id=games_category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this Category. Please create your own Category in order to edit.');}</script><body onload='myFunction()'>"  # noqa
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategorys'))
    else:
        return render_template('editCategory.html', Category=editedCategory)


# Delete a Category
@app.route('/catalog/<string:games_name>/<int:games_category_id>/delete/', methods=['GET', 'POST'])  # noqa
def deleteCategory(games_name, games_category_id):
    CategoryToDelete = session.query(
        Category).filter_by(id=games_category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if CategoryToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this Category. Please create your own Category in order to delete.');}</script><body onload='myFunction()'>"  # noqa
    if request.method == 'POST':
        session.delete(CategoryToDelete)
        flash('%s Successfully Deleted' % CategoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategorys', games_category_id=games_category_id))  # noqa
    else:
        return render_template('deleteCategory.html', Category=CategoryToDelete)  # noqa

# Show a Category menu


@app.route('/catalog/<int:games_category_id>/')
@app.route('/catalog/<int:games_category_id>/items/')
def showMenu(games_category_id):
    Categorys = session.query(Category).filter_by(id=games_category_id).one()
    creator = getUserInfo(Categorys.user_id)
    items = session.query(CategoryItem).filter_by(
        games_category_id=games_category_id).all()
    rows_num = session.query(CategoryItem).filter_by(
        games_category_id=games_category_id).count()

    if 'username' not in login_session or creator.id != login_session['user_id']:  # noqa
        return render_template('publicCategoryItem.html', items=items, Category=Categorys, creator=creator, rows_count=rows_num)  # noqa
    else:
        return render_template('CategoryItem.html', items=items, Category=Categorys, creator=creator, rows_count=rows_num)  # noqa


# Show a Item Description
@app.route('/catalog/<string:games_name>/<string:item_name>/')
def ShowItemDescription(games_name, item_name):
    Categorys = session.query(Category).filter_by(name=games_name).one()
    items = session.query(CategoryItem).filter_by(
        name=item_name).one()
    creator = getUserInfo(items.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:  # noqa
        return render_template('Item_Description.html', games_name=games_name, item_name=item_name, items=items)  # noqa
    else:
        return render_template('User_Item_Description.html', Category=Categorys, games_name=games_name, item_name=item_name, items=items)  # noqa


# Create a new menu item
@app.route('/catalog/<string:games_name>/new/', methods=['GET', 'POST'])
def newCategoryItem(games_name):
    if 'username' not in login_session:
        return redirect('/login')
    all_Categorys = session.query(Category).order_by(asc(Category.name))  # noqa
    Categorys = session.query(Category).filter_by(name=games_name).one()
    if request.method == 'POST':
        if request.form['name']:
            newItem = CategoryItem(name=request.form['name'], description=request.form['description'], games_category_id=request.form['Category_id'], user_id=login_session['user_id'])  # noqa
            session.add(newItem)
            session.commit()
            flash('New Menu %s Item Successfully Created' % (newItem.name))
            return redirect(url_for('showMenu', games_category_id=Categorys.id))  # noqa
    else:
        return render_template('newCategoryItem.html', games_category_name=games_name, Categorys=all_Categorys)  # noqa

# Edit a menu item


@app.route('/catalog/<string:games_category_name>/<string:games_item_name>/edit', methods=['GET', 'POST'])  # noqa
def editCategoryItem(games_category_name, games_item_name):  # noqa
    if 'username' not in login_session:
        return redirect('/login')
    all_Categorys = session.query(Category).order_by(asc(Category.name))  # noqa
    editedItem = session.query(CategoryItem).filter_by(name=games_item_name).one()  # noqa
    Categorys = session.query(Category).filter_by(name=games_category_name).one()  # noqa
    if login_session['user_id'] != editedItem.user_id:  # noqa
        return "<script>function myFunction() {alert('You are not authorized to edit menu items to this Category. Please create your own Category in order to edit items.');}</script><body onload='myFunction()'>"  # noqa
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']  # noqa
        if request.form['description']:
            editedItem.description = request.form['description']  # noqa
        if request.form['Category_id']:
            editedItem.games_category_id = request.form['Category_id']  # noqa
        session.add(editedItem)  # noqa
        session.commit()
        flash('Menu Item Successfully Edited')  # noqa
        return redirect(url_for('showMenu', games_category_id=Categorys.id))  # noqa
    else:
        return render_template('editCategoryItem.html', games_category_name=games_category_name, games_item_name=games_item_name, item=editedItem, Categorys=all_Categorys)  # noqa


# Delete a menu item
@app.route('/catalog/<string:games_category_name>/<string:games_item_name>/delete', methods=['GET', 'POST'])  # noqa
def deleteCategoryItem(games_category_name, games_item_name):
    if 'username' not in login_session:
        return redirect('/login')
    Categorys = session.query(Category).filter_by(name=games_category_name).one()  # noqa
    itemToDelete = session.query(CategoryItem).filter_by(name=games_item_name).one()  # noqa
    if login_session['user_id'] != itemToDelete.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete menu items to this Category. Please create your own Category in order to delete items.');}</script><body onload='myFunction()'>"  # noqa
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', games_category_id=Categorys.id))
    else:
        return render_template('deleteCategoryItem.html', item=itemToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategorys'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategorys'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

"""Import packages and modules."""
from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import os
from bson.objectid import ObjectId

############################################################
# TODO:
############################################################
# Input verification/pass length etc
# Create delete user functionality
# Hash Passwords
# Edit bio functionality
# Some kind of feedback when signed up "thanks for signing up! on homepage"
# Refactor to use modules, clean up code

############################################################
# SETUP
############################################################

"""Configure app variables."""
app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config["MONGO_URI"] = "mongodb://localhost:27017/plantsDatabase"
mongo = PyMongo(app)

# Define flask-login config variables & instantiate LoginManager
login_manager = LoginManager(app)
login_manager.init_app(app)


# Define User class
class User(UserMixin):
    """Define User class based on UserMixIn."""

    user_database = mongo.db.users

    def __init__(self, email, password, id):
        """Initialize user properties."""
        self.email = email
        self.password = password
        self.id = id


# Define flask-login user_loader config function
@login_manager.user_loader
def load_user(id):
    """Define user callback for user_loader function."""
    return mongo.db.users.find_one({'_id': ObjectId(id)})


# Define secret key in order to use flask-login
app.config.update(
    SECRET_KEY=os.urandom(24)
)

############################################################
# ROUTES
############################################################


@app.errorhandler(404)
def oops_page(e):
    """Return custom 404 page if page not found."""
    print(e)
    return render_template('404.html')


@app.route('/')
def plants_list():
    """Display the plants list page."""
    plants_data = mongo.db.plants.find()

    context = {
        'plants': plants_data,
    }
    return render_template('plants_list.html', **context)


@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    """Display user sign up page."""
    if request.method == 'GET':
        return render_template('sign_up.html')
    else:
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        user_email = request.form['user_email']
        pass_one = request.form['set-password']
        pass_two = request.form['confirm-password']
        user_password = ''
        if pass_one and pass_two and pass_one == pass_two:
            user_password = pass_one
            new_user = {
                'email': user_email,
                'password': user_password,
                'first_name': first_name,
                'last_name': last_name
            }
            insert_user = mongo.db.users.insert_one(new_user)
            user_id = insert_user.inserted_id
            get_user = mongo.db.users.find_one_or_404({'_id': ObjectId(user_id)})
            user = User(get_user['email'], get_user['password'], user_id)
            login_user(user)
            session['logged_in'] = True
            return redirect(url_for('plants_list'))
        else:
            flash('Passwords do not match. Please try again.')


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    """Allow user to access more website features."""
    if request.method == 'GET':
        return render_template('user_login.html')
    else:
        email = request.form['user_email']
        user = mongo.db.users.find_one({'email': email})
        try:
            if request.form['password'] == user['password'] and email:
                session_user = User(user['email'], user['password'], user['_id'])
                login_user(session_user)
                session['logged_in'] = True
                return redirect(url_for('create'))
            else:
                print('Something went wrong - we at the else statement.')
                return redirect(url_for('user_login'))
        except(TypeError):
            flash('Incorrect email or password, please try again.')

            context = {
                'message': 'Incorrect email or password, please try again.'
            }
            return render_template('user_login.html', **context)


@app.route('/user', methods=['GET', 'POST'])
def user():
    """Return user profile template."""
    if session['logged_in']:
        user = current_user
    else:
        print(current_user)
        return("user is none")

    context = {
        'user': user,
    }

    return render_template('user.html', **context)


@app.route('/log_out', methods=['GET', 'POST'])
def log_out():
    """Log out user."""
    logout_user()
    return redirect(url_for('plants_list'))


@app.route('/delete_user')
def delete_user():
    """Delete user profile and log out user."""
    pass


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Display the plant creation page & process data from the creation form."""
    try:
        if not session['logged_in']:
            print(f"Current user from create: {current_user}")
            print(f"Session id from create: {session.get('user_id')}")
            return redirect(url_for('user_login'))
        elif request.method == 'POST' and current_user:
            name = request.form['plant_name']
            variety = request.form['variety']
            photo_url = request.form['photo']
            date_planted = request.form['date_planted']

            new_plant = {
                'name': name,
                'photo_url': photo_url,
                'date_planted': date_planted,
                'variety': variety
            }

            plant = mongo.db.plants.insert_one(new_plant)
            plant_id = plant.inserted_id

            return redirect(url_for('detail', plant_id=plant_id))

        else:
            return render_template('create.html')
    except(KeyError):
        print('Something went wrong loading Create')
        return render_template('plants_list.html')


@app.route('/plant/<plant_id>')
def detail(plant_id):
    """Display the plant detail page & process data from the harvest form."""
    plant_to_show = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})
    harvests = mongo.db.harvests.find({"plant_id": ObjectId(plant_id)})

    context = {
        'plant': plant_to_show,
        'harvests': harvests,
        'plant_id': ObjectId(plant_id),
    }
    return render_template('detail.html', **context)


@app.route('/harvest/<plant_id>', methods=['POST'])
def harvest(plant_id):
    """Accept a POST request with data for 1 harvest and inserts into database."""
    date_harvested = request.form['date_harvested']
    plant = mongo.db.plants.find_one({'_id': ObjectId(plant_id)})

    new_harvest = {
        'quantity': f"{request.form['harvested_amount']} {plant['name']}",
        'date': date_harvested,
        'plant_id': ObjectId(plant_id)
    }

    mongo.db.harvests.insert_one(new_harvest)
    return redirect(url_for('detail', plant_id=plant_id))


@app.route('/edit/<plant_id>', methods=['GET', 'POST'])
def edit(plant_id):
    """Shows the edit page and accepts a POST request with edited data."""
    if request.method == 'POST':
        new_name = request.form['plant_name']
        new_variety = request.form['variety']
        new_photo = request.form['photo']
        new_date = request.form['date_planted']
        updated_plant = mongo.db.plants.update({'_id': ObjectId(plant_id)},
                                               {'$set': {
                                                    'name': new_name,
                                                    'variety': new_variety,
                                                    'photo_url': new_photo,
                                                    'date_planted': new_date
                                                   }
                                                })

        return redirect(url_for('detail', plant_id=plant_id))
    else:
        plant_to_show = mongo.db.plants.find_one({'_id': ObjectId(plant_id)})

        context = {
            'plant': plant_to_show
        }

        return render_template('edit.html', **context)


@app.route('/delete/<plant_id>', methods=['POST'])
def delete(plant_id):
    """Delete current plant."""
    plant_to_delete = mongo.db.plants.delete_one({'_id': ObjectId(plant_id)})
    harvests_to_delete = mongo.db.harvests.delete_many(
                                           {'plant_id': ObjectId(plant_id)})

    return redirect(url_for('plants_list'))


if __name__ == '__main__':
    app.run(debug=True)

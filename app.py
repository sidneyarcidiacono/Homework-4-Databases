from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

############################################################
# TODO:
############################################################
# Input verification
# Add login page when adding plant (cannot add plant if not logged in)
# Add more resources to db

############################################################
# SETUP
############################################################

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/plantsDatabase"
mongo = PyMongo(app)

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


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Display the plant creation page & process data from the creation form."""
    if request.method == 'POST':
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

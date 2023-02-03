from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ..forms import CarForm
from ..models import Car, db
from ..helpers import wiki_how_generator



site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    my_car = CarForm()
    try:
        if request.method == "POST" and my_car.validate_on_submit():
            make = my_car.make.data.title().strip()
            model = my_car.model.data.title().strip()
            year = my_car.year.data
            color = my_car.color.data.title().strip()
            your_mission = wiki_how_generator()
            user_token = current_user.token

            car = Car(make, model, year, color, your_mission, user_token)

            db.session.add(car)
            db.session.commit()

            return redirect(url_for('site.profile'))

    except:
        raise Exception("We aint takin that car! Try again pal!")

    user_token = current_user.token
    cars = Car.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=my_car, cars=cars)
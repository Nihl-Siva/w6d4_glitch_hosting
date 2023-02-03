from flask import Blueprint, request, jsonify
from car_collection.helpers import token_required, wiki_how_generator
from car_collection.models import db, Car, car_schema, cars_schema


api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}


@api.route('/cars', methods = ['POST'])
@token_required
def create_car(our_user):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    your_mission = wiki_how_generator()
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    car = Car(make, model, year, color, your_mission, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(our_user):
    owner = our_user.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(our_user, id):
    owner = our_user.token
    if owner == our_user.token:
        cars = Car.query.get(id)
        response = car_schema.dump(cars)
        return jsonify(response)
    else:
        return jsonify({'message': 'Ya need an ID to get in here kid....'}), 401

@api.route('/cars/<id>', methods = ['PUT', 'POST'])
@token_required
def update_car(our_user, id):
        car = Car.query.get(id)
        car.make = request.json['make']
        car.model = request.json['model']
        car.year = request.json['year']
        car.color = request.json['color']
        car.your_mission = wiki_how_generator()
        car.user_token = our_user.token

        db.session.commit()
        response = car_schema.dump(car)
        return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(our_user, id):
        car = Car.query.get(id)
        db.session.delete(car)
        db.session.commit()

        response = car_schema.dump(car)
        return jsonify(response)

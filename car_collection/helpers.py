from functools import wraps
import secrets
from flask import request, jsonify, json
from car_collection.models import User
import decimal
import requests


def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
            print(token)

        if not token:
            return jsonify({'message': 'No dice!'}), 401

        try:
            our_user = User.query.filter_by(token = token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Nah fish!'})

        except:
            owner = User.query.filter_by(token=token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'NOT TODAY SATAN!'})
        return our_flask_function(our_user, *args, **kwargs)
    return decorated

def wiki_how_generator():
    
    url = "https://hargrimm-wikihow-v1.p.rapidapi.com/steps"

    querystring = {"count":"3"}

    headers = {
        "X-RapidAPI-Key": "dd32d3ce01msh09c4725f53a9d2dp186958jsn12c9c67e941a",
        "X-RapidAPI-Host": "hargrimm-wikihow-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()
    return f"1. {data['1']} 2. {data['2']} 3. {data['3']}"

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)
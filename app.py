from flask import Flask, jsonify
from db import db
from models import User, History
from flask_cors import CORS
from flask import request
from crawler import Crawler
from classifier import predict_class, get_three_docs
from poor_me import reference
from flask_jwt import JWT, jwt_required, current_identity
from datetime import timedelta


def authenticate(username, password):
    user = User.query.filter(User.username == username).scalar()
    if (user.password == password):
        return user


def identity(payload):
    print()
    return User.query.filter(User.id == payload['identity']).scalar()


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://recipe-sorting-hat:asdfjkl;@1234@tg-proxy.yuching.app/recipe-sorting-hat'
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=24)
db.init_app(app)
CORS(app)

jwt = JWT(app, authenticate, identity)


@app.route('/user', endpoint='user')
@jwt_required()
def index():
    data = {"nickname": current_identity.nickname}
    return jsonify(data)


@app.route('/search_by_url', endpoint='search_by_url')
@jwt_required()
def index():
    key_dict = {
        1: 'American',
        2: 'Chinese',
        3: 'French',
        4: 'Indian',
        5: 'Italian',
        6: 'Japanese',
        7: 'Korean',
        8: 'Southeast_Asia',
        9: 'Mexican',
        10: 'Middle_Eastern',
        11: 'Spanish',
    }
    url = request.args.get('url')
    # result = Crawler('https://www.myrecipes.com/recipe/morcilla').get_data()
    text = Crawler(url).get_data()

    number = predict_class(text)

    result = {
        'result_type': key_dict[number],
        'docs': get_three_docs(number - 1)
    }

    return jsonify(result)


@app.route('/search_by_keywords', endpoint='search_by_keywords')
@jwt_required()
def index():
    keywords = request.args.get('keywords')
    print(keywords)
    return jsonify(reference(keywords))

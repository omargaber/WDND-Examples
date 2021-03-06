import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import json

from models import setup_db, Account
from validation import *


def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    #     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    #     return response
    # __________________________________________________AUTH0__________________________________________________

    # ___________________________________________________AUTH___________________________________________________

    def get_token_auth_header():
        # Check if Authorization is present in the header or not
        if 'Authorization' not in request.headers:
            abort(401)

        auth_header = request.headers['Authorization'].split(' ')
        # print(auth_header)

        if len(auth_header) != 2:
            abort(401)
        elif auth_header[0].lower() != 'bearer':
            abort(401)

        return auth_header[1]

    def requires_auth(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            # print('----------------------------------------------')
            # print(jwt)
            # print('----------------------------------------------')
            try:
                payload = verify_decode_jwt(jwt)
                print('----------------------------------------------')
                print(payload)
                print('----------------------------------------------')
            except:
                abort(401)
            return f(payload, *args, **kwargs)
        return wrapper

    # ______________________________________________________________________________________________________

    @app.route('/')
    @requires_auth
    def index(jwt):
        return jsonify({
            'success': True,
            'message': 'Hello Udacians'
        })

    @app.route('/accounts')
    def retrieve_accounts():

        user_accounts = Account.query.count()

        # if user_accounts == 0:
        #     abort(404)

        return jsonify({
            'success': True,
            'total_accounts': user_accounts
        })

    @app.route('/accounts/<account_id>', methods=['PATCH'])
    def edit_account_first_name(account_id):
        account = Account.query.get(account_id)
        body = request.get_json()
        first_name = body.get("first_name", None)
        account.first_name = first_name
        account.update()
        return jsonify({'success': True, 'first_name': first_name})

    @app.route('/accounts/create', methods=['POST'])
    def create_account():
        body = request.get_json()
        first_name = body.get("first_name", None)
        last_name = body.get("last_name", None)
        init_balance = body.get("balance", None)
        search = body.get('search', None)

        # if first_name is None or last_name is None or init_balance is None:
        #     abort(400)

        res_body = {}

        # TDD Example
        if search:
            selection = Account.query.filter(
                Account.first_name.contains(search)).count()

            return jsonify({
                "success": True,
                "total_records": selection
            })

        else:
            error = False
            if first_name is None or init_balance is None:
                error = True
                abort(400)
            else:
                try:
                    new_account = Account(first_name=first_name,
                                          last_name=last_name, balance=init_balance)
                    new_account.insert()
                    res_body = new_account.format()
                    res_body['success'] = True

                    return jsonify(res_body)

                except:
                    abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    return app

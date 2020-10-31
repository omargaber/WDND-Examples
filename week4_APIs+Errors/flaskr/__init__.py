import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Account


def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)
    # CORS(app, resources={r"*/accounts*": {origins: '*'}})
    # Lets try CORS

    CORS(app, resources={"/": {'origins': ['https://example.com']}})
    # CORS(app, origins='https://example.com')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, PUT, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    # In case we want to apply cors to a specific endpoint
    # @cross_origin()
    def index():
        return jsonify({
            'success': True,
            'message': 'Hello World'
        })

    @app.route('/accounts')
    def retrieve_accounts():

        user_accounts = Account.query.count()

        return jsonify({
            'success': True,
            'total_accounts': user_accounts
        })

    @app.route('/accounts/create', methods=['POST'])
    def create_account():
        # Demonstrate the Werkzeug issue
        body = request.get_json()
        
        if body is None:
            error=True
            abort(400)
        
        first_name = body.get("first_name", None)
        last_name = body.get("last_name", None)
        init_balance = int(body.get("balance", 0))

        
        # try:
        #     first_name = request.get_json()['first_name']
        #     last_name = request.get_json()['last_name']
        #     init_balance = int(request.get_json()['balance'])
        # except:
        #     abort(400)

        res_body = {}

        error = False
        if first_name is None or init_balance is None or last_name is None:
            error = True
            abort(400)
        else:
            try:
                new_account = Account(first_name=first_name,
                                      last_name=last_name, balance=init_balance)
                # Using the class method
                new_account.insert()
                
                # res_body = new_account.format()
                res_body['account_id'] = new_account.id
                res_body['first_name'] = new_account.first_name
                res_body['last_name'] = new_account.last_name
                res_body['balance'] = new_account.balance
                res_body['success'] = True

                return jsonify(res_body)

            except:
                abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400
    
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    # Add a method not allowed handler and try it

    # Add an internal server error handler and try it

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    
    return app

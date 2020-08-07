import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Account


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

    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'Hello World'
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

    @app.route('/accounts/create', methods=['POST'])
    def create_account():
        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        init_balance = request.get_json()['balance']

        res_body = {}

        error = False
        if first_name is None or init_balance is None:
            error = True
            abort(400)
        else:
            try:
                new_account = Account(first_name=first_name,
                                      last_name=last_name, balance=init_balance)
                db.session.add(new_account)
                db.session.commit()
                res_body['created'] = new_account.id
                res_body['first_name'] = new_account.first_name
                res_body['last_name'] = new_account.last_name
                res_body['balance'] = new_account.balance
                res_body['success']: True

                return jsonify(res_body)

            except:
                abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app

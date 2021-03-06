from flask import jsonify, g, request, current_app
from app import db, jwt
from app.models import User
from app.api import bp
from app.api.auth import verify_refresh_request

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity

import time


@bp.route('/login', methods=['POST'])
def get_token():
    """
    This endpoint is used for users to get bearer tokens

    This request receives a email and password for login purposes, and uses the auth.verify_password function in the
    'auth' module. If the return is True (email and password are correct), we then call the get token method to retrieve
    the existing token, or generate a new one if it is expiring or expired
    """

    # Checks if there is a body
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # Gets the username and password, and defaults to null
    country_code = request.json.get('countryCode', None)
    phone_number = request.json.get('phoneNumber', None)
    password = request.json.get('password', None)

    # Validation in case the user didn't include anything
    if not country_code:
        return jsonify({"msg": "Missing countryCode parameter"}), 400
    if not phone_number:
        return jsonify({"msg": "Missing phoneNumber parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    # Tries to find a user by the given email
    user = User.query.filter(User.full_phone_number == '+' + country_code + phone_number).first()
    # Returns false if the user does not exist
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Phone number or password is incorrect"}), 401

    # Generates the access token
    access_token = create_access_token(identity='+'+country_code+phone_number)
    refresh_token = create_refresh_token(identity='+'+country_code+phone_number)

    # Returns the access token
    return jsonify({
        'token': access_token,
        'expires_at': int(time.time()) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] - 1,
        'refresh_token': refresh_token
    }), 200

@bp.route('/refresh', methods=['GET'])
@verify_refresh_request
def refresh_token():
    current_user = get_jwt_identity()
    return jsonify({
        'token': create_access_token(identity=current_user),
        'expires_at': int(time.time()) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] - 1,
        'refresh_token': create_refresh_token(identity=current_user)
    }), 200

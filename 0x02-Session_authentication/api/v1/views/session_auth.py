#!/usr/bin/env python3
""" Module of Users views
"""
import os
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def auth_session():
    """
    This Method Handle user login.
    """
    one_email = request.form.get("email")
    one_password = request.form.get("password")
    if one_email is None or one_email == "":
        return jsonify({"error": "email missing"}), 400
    if one_password is None or one_password == "":
        return jsonify({"error": "password missing"}), 400
    one_users = User.search({"email": one_email})
    if not one_users or one_users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in one_users:
        if user.is_valid_password(one_password):
            from api.v1.app import auth

            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv("SESSION_NAME")
            resp.set_cookie(session_name, session_id)
            return resp
    return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def handle_logout():
    """
    THis Method Handle user logout.
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)

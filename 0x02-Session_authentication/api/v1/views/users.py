#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users."""
    one_all_users = [user.to_json() for user in User.all()]
    return jsonify(one_all_users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/:id."""
    if user_id is None:
        abort(404)
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        one_user = request.current_user
        return jsonify(one_user.to_json())
    one_user = User.get(user_id)
    if one_user is None:
        abort(404)
    if request.current_user is None:
        abort(404)
    return jsonify(one_user.to_json())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id."""
    if user_id is None:
        abort(404)
    one_user = User.get(user_id)
    if one_user is None:
        abort(404)
    one_user.remove()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/."""
    one_rj = None
    one_error_msg = None
    try:
        one_rj = request.get_json()
    except Exception as e:
        one_rj = None
    if one_rj is None:
        one_error_msg = "Wrong format"
    if one_error_msg is None and one_rj.get("email", "") == "":
        one_error_msg = "email missing"
    if one_error_msg is None and one_rj.get("password", "") == "":
        one_error_msg = "password missing"
    if one_error_msg is None:
        try:
            user = User()
            user.email = one_rj.get("email")
            user.password = one_rj.get("password")
            user.first_name = one_rj.get("first_name")
            user.last_name = one_rj.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            one_error_msg = "Can't create User: {}".format(e)
    return jsonify({"error": one_error_msg}), 400


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id."""
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    one_rj = None
    try:
        one_rj = request.get_json()
    except Exception as e:
        one_rj = None
    if one_rj is None:
        return jsonify({"error": "Wrong format"}), 400
    if one_rj.get("first_name") is not None:
        user.first_name = one_rj.get("first_name")
    if one_rj.get("last_name") is not None:
        user.last_name = one_rj.get("last_name")
    user.save()
    return jsonify(user.to_json()), 200

from flask import Blueprint, request, make_response, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from flasgger import swag_from

from models import User

bp = Blueprint('auth', __name__)


def admin_required(function):
    """Decorator function that takes care of verifying that the logged in user is of type admin.

    :param function: the view function where login is required and the user is of type admin
    :return: if the user is of type admin, the function passed as a parameter otherwise responds with status code 403
    """
    def wrapper():
        user = current_user
        role = user.role.name

        if role == "admin":
            return function()
        return make_response(jsonify({"message": "Reserved area for admin users."}), 403)

    wrapper.__name__ = function.__name__
    return wrapper


@bp.route("login", methods=["POST"])
@swag_from("../docs/login.yml")
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    user = User.query.filter_by(username=username).first()
    if user:
        if user.password == password:
            login_user(user)
            return make_response(jsonify({"message": "Login successful"}), 200)
    return make_response(jsonify({"message": "User not found. Username or Password Error"}), 404)


@bp.route('logout', methods=["POST"])
@login_required
@swag_from("../docs/logout.yml")
def logout():
    logout_user()
    return make_response(jsonify({"message": "Logout successful"}), 200)

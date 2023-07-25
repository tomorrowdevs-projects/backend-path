from flask import Blueprint

from views.auth import token_required

bp = Blueprint("index", __name__)


@bp.route("")
def homepage():
    return "This is the homepage and it is an unprotected route."


@bp.route("protected-area")
@token_required
def protected_area():
    return "Welcome in the protected area."

from flask import Blueprint
from flasgger import swag_from

from views.auth import token_required

bp = Blueprint("index", __name__)


@bp.route("")
@swag_from("../docs/homepage.yml")
def homepage():
    return "This is the homepage and it is an unprotected route."


@bp.route("protected-area")
@swag_from("../docs/protected_area.yml")
@token_required
def protected_area():
    return "Welcome in the protected area."

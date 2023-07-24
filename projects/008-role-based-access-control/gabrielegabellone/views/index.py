from flask import Blueprint
from flask_login import login_required, current_user
from flasgger import swag_from

from views.auth import admin_required

bp = Blueprint('index', __name__)


@bp.route("regular-area")
@login_required
@swag_from("../docs/regular_area.yml")
def regular_area():
    return f"Welcome to the regular area, {current_user.username}."


@bp.route("admin-area")
@login_required
@swag_from("../docs/admin_area.yml")
@admin_required
def admin_area():
    return f"Welcome to the admin area, {current_user.username}."

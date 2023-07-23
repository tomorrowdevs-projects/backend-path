from flask import Blueprint
from flask_login import login_required, current_user

from views.auth import admin_required

bp = Blueprint('index', __name__)


@bp.route("regular-area")
@login_required
def regular_area():
    return f"Welcome to the regular area, {current_user.username}."


@bp.route("admin-area")
@login_required
@admin_required
def admin_area():
    return f"Welcome to the admin area, {current_user.username}."

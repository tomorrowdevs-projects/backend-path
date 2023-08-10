from flask import Blueprint, session

from views.auth import login_required

bp = Blueprint("index", __name__)


@bp.route('/protected_area')
@login_required
def protected_area():
    return f'Welcome to the protected area, {session["name"]} <a href="/auth/logout"?><button>Logout</button></a>'

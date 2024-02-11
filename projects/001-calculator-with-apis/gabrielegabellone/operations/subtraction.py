from flask import Blueprint, request, make_response, jsonify
from flasgger import swag_from

bp = Blueprint('subtraction', __name__)


@bp.route("", methods=["POST"])
@swag_from("../docs/subtraction.yml")
def subtraction():
    data = request.get_json()
    try:
        minuend = data["minuend"]
        subtrahends = data["subtrahends"]

        difference = minuend
        for s in subtrahends:
            difference -= s
            minuend = difference

        return make_response(jsonify({"result": difference}), 200)
    
    except TypeError:
        return make_response(jsonify({"msg": "One or more invalid values. Only integers or decimals are allowed."}), 400)

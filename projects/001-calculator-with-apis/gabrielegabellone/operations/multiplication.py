from flask import Blueprint, request, make_response, jsonify
from flasgger import swag_from

bp = Blueprint('multiplication', __name__)


@bp.route("", methods=["POST"])
@swag_from("../docs/multiplication.yml")
def multiplication():
    data = request.get_json()
    try:
        multiplicand = data["multiplicand"]
        multiplicators = data["multiplicators"]

        product = multiplicand     
        for m in multiplicators:
            if type(m) not in [int, float]:
                raise TypeError
            product *= m

        return make_response(jsonify({"result": product}), 200)
    
    except TypeError:
        return make_response(jsonify({"msg": "One or more invalid values. Only integers or decimals are allowed."}), 400)

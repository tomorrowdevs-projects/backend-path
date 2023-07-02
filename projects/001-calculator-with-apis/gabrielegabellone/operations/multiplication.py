from flask import Blueprint, request, make_response, jsonify

bp = Blueprint('multiplication', __name__)

@bp.route("", methods=["POST"])
def multiplication():
    data = request.get_json()
    try:
        multiplicand = data["multiplicand"]
        multiplicators = data["multiplicators"]

        product = multiplicand     
        for m in multiplicators:
            product *= m

        return make_response(jsonify({"result": product}), 200)
    
    except TypeError:
        return make_response(jsonify({"msg": "One or more invalid values. Only integers or decimals are allowed."}), 400)

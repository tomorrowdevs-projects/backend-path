from flask import Blueprint, request, make_response, jsonify

bp = Blueprint('addition', __name__)


@bp.route("", methods=["POST"])
def addition():
    data = request.get_json()
    try:
        numbers = data["addends"]
        result = sum(numbers)
        return make_response(jsonify({"result": result}), 200)
     
    except TypeError:
        return make_response(jsonify({"msg": "One or more invalid values. Only integers or decimals are allowed."}), 400)

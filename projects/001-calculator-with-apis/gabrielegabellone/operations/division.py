from flask import Blueprint, request, make_response, jsonify
from flasgger import swag_from

bp = Blueprint('division', __name__)


@bp.route("", methods=["POST"])
@swag_from("../docs/division.yml")
def division():
    data = request.get_json()
    try:
        dividend = data["dividend"]
        divisors = data["divisors"]

        quotient = dividend
        for d in divisors:
            quotient /= d

        return make_response(jsonify({"result": quotient}), 200)
    
    except TypeError:
        return make_response(jsonify({"msg": "One or more invalid values. Only integers or decimals are allowed."}), 400)
    
    except ZeroDivisionError:
        return make_response(jsonify({"msg": "You cannot divide a number by 0."}), 400)
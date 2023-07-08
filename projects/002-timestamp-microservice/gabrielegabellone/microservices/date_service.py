import datetime
import time

from flask import Blueprint, request, jsonify, make_response
from flasgger import swag_from

bp = Blueprint("date_bp", __name__)
today = datetime.date.today()


def from_datetime_to_utc(date_to_convert: datetime.datetime) -> str:
    """Takes care of converting from a date into a string in a format like this: 'Fri, 25 Dec 2015 00:00:00 GMT'.
    
    :param date_to_convert: the date to convert to string
    :return: the string representing the date
    """ 
    utc = date_to_convert.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return utc


@bp.route("/:date")
@swag_from("../docs/from_date_to_unix_and_utc.yml")
def from_date_to_unix_and_utc():
    args = request.args

    year = args.get("year", default=today.year, type=int)
    month = args.get("month", default=today.month, type=int)
    day = args.get("day", default=today.day, type=int)

    try:
        date_to_convert = datetime.date(year=year, month=month, day=day)
        unix_timestamp = time.mktime(date_to_convert.timetuple())
        utc = from_datetime_to_utc(date_to_convert)
        return jsonify({"unix": unix_timestamp, "utc": utc})
    except ValueError:
        return make_response(jsonify({"error": "Invalid Date"}), 400)


@bp.route("/<int:unix_timestamp>")
@swag_from("../docs/from_unix_to_utc.yml")
def from_unix_to_utc(unix_timestamp: int):
    try:
        utc_date = datetime.datetime.utcfromtimestamp(unix_timestamp)
        formatted_utc_date = from_datetime_to_utc(utc_date)
        return jsonify({"unix": unix_timestamp, "utc": formatted_utc_date})
    except OSError:
        return make_response(jsonify({"error": "unix timestamp not valid"}), 400)

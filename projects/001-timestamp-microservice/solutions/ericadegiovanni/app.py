# A request to /api/:date? with a valid date should return:
# { unix: 1451001600000, utc: "Fri, 25 Dec 2015 00:00:00 GMT" }
# A request to /api/1451001600000 should return { unix: 1451001600000, utc: "Fri, 25 Dec 2015 00:00:00 GMT" }
# If the input date string is invalid, the api returns an object having the structure { error : "Invalid Date" }


from datetime import datetime, timezone
import dateutil
from dateutil.parser import parse
from flask import Flask, jsonify

app = Flask(__name__)


def date_parser(date_str):
    
    """
    param: string representing a date
    return a datetime object
    raise a ParserError if the string is not valid
    """
    if date_str.isnumeric():
        d = datetime.fromtimestamp(int(date_str)/1000, tz=timezone.utc)
        return d
    else:       
        d = parse(date_str)
        return d
        
    
def date2json(date_obj):

    """
    param: datetime object
    return a JSON object with a unix and a utc key
    """
    
    unix = int(date_obj.timestamp()) * 1000
    res = {"unix": unix, "utc": date_obj}  
    return jsonify(res)
    
 
#An empty date parameter should return the current time in a JSON object with a unix and utc key
@app.route("/api/")
def index():
    d = datetime.now()
    res = date2json(d) 
    return res


@app.route('/api/<date>')
def date(date):
    try:
        d = date_parser(date)
        return date2json(d)
    except Exception:     
        return jsonify(error="Invalid Date")
          

if __name__ == "__main__":
    app.run(debug=True)
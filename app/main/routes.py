import datetime
import json

import dateutil.parser
from flask import abort, current_app, request

from app import db
from app.models import SensorReading
from app.main import bp


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


@bp.route("/")
@bp.route("/index")
def index():
    return "Hello World!"


@bp.route("/api/send")
def send():
    if request.args.get("api_key") != current_app.config["API_KEY"]:
        return abort("Invalid API KEY!")
    else:
        if "timestamp" in request.args:
            timestamp = dateutil.parser.parse(request.args["timestamp"])
        else:
            timestamp = None
        for key, value in request.args.items(multi=True):
            if key.endswith("_reading"):
                sensor = key[: -len("_reading")]
                tokens = value.split(":", 1)
                msg = {"sensor": sensor, "value": float(tokens[0]), "timestamp": timestamp}
                if len(tokens) > 1:
                    msg["unit"] = tokens[1]
                msg = json.loads(json.dumps(msg, cls=DateTimeEncoder))
                r = SensorReading(device_id=request.args["device_id"], msg=msg)
                print("STORING", msg)
                db.session.add(r)
        db.session.commit()
        return "OK"


@bp.route("/api/list")
def list_():
    result = []
    result = list(map(lambda r: str(vars(r)), SensorReading.query.all()))
    return "\n".join(result)

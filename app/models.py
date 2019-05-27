import datetime
from sqlalchemy.dialects.postgresql import JSONB

from app import db


class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    device_id = db.Column(db.String(64), index=True)
    msg = db.Column(JSONB)

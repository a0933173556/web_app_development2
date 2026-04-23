from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .event import Event
from .registration import Registration

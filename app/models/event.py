from datetime import datetime
from . import db

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # 建立與 Registration 的關聯，當活動刪除時，自動刪除相關的報名資料 (cascade='all, delete-orphan')
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade='all, delete-orphan')

    @classmethod
    def create(cls, title, description, location, start_time, end_time, capacity=None):
        new_event = cls(
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
            capacity=capacity
        )
        db.session.add(new_event)
        db.session.commit()
        return new_event

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, event_id):
        return cls.query.get(event_id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

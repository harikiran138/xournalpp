from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Session(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    data = db.Column(db.Text, nullable=True) # JSON string of board elements

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "data": self.data
        }

class Recording(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    filepath = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.Integer, default=0) # in seconds
    thumbnail_path = db.Column(db.String(500), nullable=True)
    metadata_json = db.Column(db.Text, nullable=True) # JSON string

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "filepath": self.filepath,
            "duration": self.duration,
            "thumbnail_path": self.thumbnail_path,
            "metadata": json.loads(self.metadata_json) if self.metadata_json else {}
        }

class Section(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    recording_id = db.Column(db.String(36), db.ForeignKey('recording.id'), nullable=False)
    name = db.Column(db.String(200), nullable=True)
    start_ms = db.Column(db.Integer, nullable=False)
    end_ms = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    thumbnail_path = db.Column(db.String(500), nullable=True)
    ai_summary = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "recording_id": self.recording_id,
            "name": self.name,
            "start_ms": self.start_ms,
            "end_ms": self.end_ms,
            "notes": self.notes,
            "thumbnail_path": self.thumbnail_path,
            "ai_summary": self.ai_summary
        }

class Model3D(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    metadata_json = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "filepath": self.filepath,
            "metadata": json.loads(self.metadata_json) if self.metadata_json else {}
        }

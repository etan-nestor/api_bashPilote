from datetime import datetime
from app.extensions import db

class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    logs = db.relationship('ScriptLog', backref='script', lazy=True, cascade='all, delete-orphan')
    jobs = db.relationship('Job', backref='script', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ScriptLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    script_id = db.Column(db.Integer, db.ForeignKey('script.id'), nullable=False)
    output = db.Column(db.Text)
    return_code = db.Column(db.Integer)
    execution_time = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'script_id': self.script_id,
            'output': self.output,
            'return_code': self.return_code,
            'execution_time': self.execution_time,
            'timestamp': self.timestamp.isoformat()
        }



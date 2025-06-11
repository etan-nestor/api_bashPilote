from datetime import datetime
from app.extensions import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    script_id = db.Column(db.Integer, db.ForeignKey('script.id'), nullable=False)
    cron_expression = db.Column(db.String(50))
    next_run_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'script_id': self.script_id,
            'cron_expression': self.cron_expression,
            'next_run_time': self.next_run_time.isoformat() if self.next_run_time else None
        }
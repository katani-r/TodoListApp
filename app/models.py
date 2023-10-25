from datetime import datetime
from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default='未完了')  # Default to '未完了', which means 'Not Completed'

    def __repr__(self):
        return f'<Task {self.title}>'

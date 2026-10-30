from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    summaries = db.relationship('Summary', backref='user', lazy=True, cascade='all, delete-orphan')

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200))
    original_text = db.Column(db.Text, nullable=False)
    summary_text = db.Column(db.Text, nullable=False)
    method = db.Column(db.String(50))  # extractive, abstractive
    model_used = db.Column(db.String(100))
    summary_length = db.Column(db.String(20))  # short, medium, long
    original_word_count = db.Column(db.Integer)
    summary_word_count = db.Column(db.Integer)
    compression_ratio = db.Column(db.Float)
    processing_time = db.Column(db.Float)
    source_type = db.Column(db.String(20))  # text, file, url
    source_filename = db.Column(db.String(200))
    source_url = db.Column(db.String(500))
    keywords = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'original_word_count': self.original_word_count,
            'summary_word_count': self.summary_word_count,
            'compression_ratio': self.compression_ratio,
            'method': self.method,
            'model_used': self.model_used,
            'summary_length': self.summary_length,
            'processing_time': self.processing_time,
            'source_type': self.source_type,
            'source_filename': self.source_filename,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

from models.database import db, Summary
from datetime import datetime
import json

class SummaryManager:
    @staticmethod
    def save_summary(user_id, data):
        summary = Summary(
            user_id=user_id,
            title=data.get('title') or 'Untitled Summary',
            original_text=data['original_text'],
            summary_text=data['summary_text'],
            method=data['method'],
            model_used=data.get('model_used'),
            summary_length=data.get('summary_length'),
            original_word_count=data.get('original_word_count'),
            summary_word_count=data.get('summary_word_count'),
            compression_ratio=data.get('compression_ratio'),
            processing_time=data.get('processing_time'),
            source_type=data.get('source_type'),
            source_filename=data.get('source_filename'),
            source_url=data.get('source_url'),
            keywords=json.dumps(data.get('keywords', []))
        )
        db.session.add(summary)
        db.session.commit()
        return summary
    
    @staticmethod
    def get_user_summaries(user_id, limit=None):
        query = Summary.query.filter_by(user_id=user_id).order_by(Summary.created_at.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @staticmethod
    def get_summary_by_id(summary_id, user_id):
        return Summary.query.filter_by(id=summary_id, user_id=user_id).first()
    
    @staticmethod
    def delete_summary(summary_id, user_id):
        summary = Summary.query.filter_by(id=summary_id, user_id=user_id).first()
        if summary:
            db.session.delete(summary)
            db.session.commit()
            return True
        return False

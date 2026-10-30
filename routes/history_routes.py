from flask import Blueprint, jsonify, session, request
from routes.auth_routes import login_required
from models.summary import SummaryManager
from services.evaluation import EvaluationService
import json

history_bp = Blueprint('history', __name__)

@history_bp.route('/api/history', methods=['GET'])
@login_required
def get_history():
    try:
        user_id = session['user_id']
        summaries = SummaryManager.get_user_summaries(user_id)
        return jsonify([s.to_dict() for s in summaries]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/api/history/<int:summary_id>', methods=['GET'])
@login_required
def get_summary_detail(summary_id):
    try:
        user_id = session['user_id']
        summary = SummaryManager.get_summary_by_id(summary_id, user_id)
        if not summary:
            return jsonify({'error': 'Summary not found'}), 404
        
        keywords = []
        if summary.keywords:
            try:
                keywords = json.loads(summary.keywords)
            except:
                keywords = []
        
        return jsonify({
            'id': summary.id,
            'title': summary.title,
            'original_text': summary.original_text,
            'summary_text': summary.summary_text,
            'method': summary.method,
            'model_used': summary.model_used,
            'summary_length': summary.summary_length,
            'original_word_count': summary.original_word_count,
            'summary_word_count': summary.summary_word_count,
            'compression_ratio': summary.compression_ratio,
            'processing_time': summary.processing_time,
            'source_type': summary.source_type,
            'source_filename': summary.source_filename,
            'source_url': summary.source_url,
            'keywords': keywords,
            'created_at': summary.created_at.strftime('%Y-%m-%d %H:%M:%S') if summary.created_at else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/api/history/<int:summary_id>', methods=['DELETE'])
@login_required
def delete_summary(summary_id):
    try:
        user_id = session['user_id']
        success = SummaryManager.delete_summary(summary_id, user_id)
        if success:
            return jsonify({'message': 'Summary deleted successfully'}), 200
        else:
            return jsonify({'error': 'Summary not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/api/evaluate', methods=['POST'])
@login_required
def evaluate():
    try:
        data = request.get_json()
        summary = data.get('summary', '')
        reference = data.get('reference', '')
        
        if not summary or not reference:
            return jsonify({'error': 'Both summary and reference are required'}), 400
        
        evaluator = EvaluationService()
        scores = evaluator.evaluate(summary, reference)
        return jsonify(scores), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

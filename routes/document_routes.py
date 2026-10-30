from flask import Blueprint, request, jsonify, session
from routes.auth_routes import login_required
from services.document_processor import DocumentProcessor
import os
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not DocumentProcessor.allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only TXT, PDF, DOCX allowed'}), 400
        
        filename = secure_filename(file.filename)
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        try:
            text = DocumentProcessor.process_file(file_path, filename)
            if not text or len(text.strip()) < 50:
                os.remove(file_path)
                return jsonify({'error': 'Extracted text is too short or empty'}), 400
            
            # Clean up file after processing
            os.remove(file_path)
            
            return jsonify({
                'text': text,
                'filename': filename,
                'length': len(text)
            }), 200
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/api/extract-url', methods=['POST'])
@login_required
def extract_url():
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        text = DocumentProcessor.extract_from_url(url)
        if not text or len(text.strip()) < 50:
            return jsonify({'error': 'Extracted content is too short'}), 400
        
        return jsonify({
            'text': text,
            'url': url,
            'length': len(text)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

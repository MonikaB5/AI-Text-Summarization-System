from flask import Blueprint, request, jsonify, session, send_file
from routes.auth_routes import login_required
from services.extractive_summarizer import TextRankSummarizer
from services.abstractive_summarizer import AbstractiveSummarizer
from services.preprocessing import TextPreprocessor
from services.keyword_extractor import KeywordExtractor
from models.summary import SummaryManager
from services.export_service import ExportService
from services.evaluation import EvaluationService
import time
import io

summarization_bp = Blueprint('summarization', __name__)

@summarization_bp.route('/api/summarize', methods=['POST'])
@login_required
def summarize():
    try:
        data = request.get_json()
        text = data.get('text', '')
        method = data.get('method', 'extractive')  # extractive or abstractive
        summary_length = data.get('summary_length', 'medium')
        source_type = data.get('source_type', 'text')
        source_filename = data.get('source_filename')
        source_url = data.get('source_url')
        title = data.get('title')
        
        if not text or len(text.strip()) < 30:
            return jsonify({'error': 'Text must be at least 30 characters long'}), 400
        
        preprocessor = TextPreprocessor()
        keyword_extractor = KeywordExtractor()
        
        start_time = time.time()
        
        original_word_count = preprocessor.get_word_count(text)
        original_sentence_count = preprocessor.get_sentence_count(text)
        
        # Calculate ratio based on summary length
        if summary_length == 'short':
            ratio = 0.2
        elif summary_length == 'long':
            ratio = 0.4
        else:
            ratio = 0.3
        
        summary_text = ''
        model_used = None
        fallback_used = False
        
        if method == 'extractive':
            summarizer = TextRankSummarizer()
            summary_text = summarizer.summarize(text, ratio=ratio)
            model_used = 'TextRank (Graph-based Sentence Ranking)'
        elif method == 'abstractive':
            try:
                summarizer = AbstractiveSummarizer()
                summary_text = summarizer.summarize(text, ratio=ratio, summary_length=summary_length)
                model_used = 'facebook/bart-large-cnn (Transformer)'
            except Exception as e:
                # Fallback to extractive
                summarizer = TextRankSummarizer()
                summary_text = summarizer.summarize(text, ratio=ratio)
                model_used = 'TextRank (fallback - transformer unavailable)'
                fallback_used = True
        else:
            return jsonify({'error': 'Invalid method. Use extractive or abstractive'}), 400
        
        # Clean up summary
        summary_sentences = preprocessor.tokenize_sentences(summary_text)
        summary_sentences = preprocessor.remove_duplicates(summary_sentences)
        summary_text = ' '.join(summary_sentences)
        
        processing_time = round(time.time() - start_time, 3)
        
        summary_word_count = preprocessor.get_word_count(summary_text)
        summary_sentence_count = preprocessor.get_sentence_count(summary_text)
        
        compression_ratio = round((1 - summary_word_count / original_word_count) * 100, 2) if original_word_count > 0 else 0
        
        keywords = keyword_extractor.extract_keywords(text, top_n=10)
        
        # Get important sentences (extractive key sentences)
        try:
            ranker = TextRankSummarizer()
            key_sentences = ranker.summarize(text, ratio=0.3)
            key_sentences_list = preprocessor.tokenize_sentences(key_sentences)
        except:
            key_sentences_list = []
        
        result = {
            'summary_text': summary_text,
            'original_word_count': original_word_count,
            'original_sentence_count': original_sentence_count,
            'summary_word_count': summary_word_count,
            'summary_sentence_count': summary_sentence_count,
            'compression_ratio': compression_ratio,
            'processing_time': processing_time,
            'method': method,
            'model_used': model_used,
            'summary_length': summary_length,
            'keywords': keywords,
            'fallback_used': fallback_used,
            'original_reading_time': round(original_word_count / 200, 2),
            'summary_reading_time': round(summary_word_count / 200, 2),
            'key_sentences': key_sentences_list[:5]
        }
        
        # Save to history
        try:
            user_id = session['user_id']
            SummaryManager.save_summary(user_id, {
                'title': title,
                'original_text': text,
                'summary_text': summary_text,
                'method': method,
                'model_used': model_used,
                'summary_length': summary_length,
                'original_word_count': original_word_count,
                'summary_word_count': summary_word_count,
                'compression_ratio': compression_ratio,
                'processing_time': processing_time,
                'source_type': source_type,
                'source_filename': source_filename,
                'source_url': source_url,
                'keywords': keywords
            })
        except Exception as e:
            pass  # Don't fail if saving to history fails
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@summarization_bp.route('/api/compare', methods=['POST'])
@login_required
def compare_summaries():
    try:
        data = request.get_json()
        text = data.get('text', '')
        summary_length = data.get('summary_length', 'medium')
        
        if not text or len(text.strip()) < 30:
            return jsonify({'error': 'Text must be at least 30 characters long'}), 400
        
        preprocessor = TextPreprocessor()
        keyword_extractor = KeywordExtractor()
        
        results = {}
        orig_words = preprocessor.get_word_count(text)
        
        if summary_length == 'short':
            ratio = 0.2
        elif summary_length == 'long':
            ratio = 0.4
        else:
            ratio = 0.3
        
        # Extractive
        start_time = time.time()
        extractive = TextRankSummarizer()
        ext_summary = extractive.summarize(text, ratio=ratio)
        ext_time = round(time.time() - start_time, 3)
        ext_words = preprocessor.get_word_count(ext_summary)
        ext_comp = round((1 - ext_words / orig_words) * 100, 2) if orig_words > 0 else 0
        
        results['extractive'] = {
            'summary_text': ext_summary,
            'word_count': ext_words,
            'compression_ratio': ext_comp,
            'processing_time': ext_time,
            'method': 'TextRank'
        }
        
        # Abstractive
        try:
            start_time = time.time()
            abstractive = AbstractiveSummarizer()
            abs_summary = abstractive.summarize(text, ratio=ratio, summary_length=summary_length)
            abs_time = round(time.time() - start_time, 3)
            abs_words = preprocessor.get_word_count(abs_summary)
            abs_comp = round((1 - abs_words / orig_words) * 100, 2) if orig_words > 0 else 0
            results['abstractive'] = {
                'summary_text': abs_summary,
                'word_count': abs_words,
                'compression_ratio': abs_comp,
                'processing_time': abs_time,
                'method': 'BART Transformer',
                'fallback': False
            }
        except Exception as e:
            results['abstractive'] = {
                'error': str(e),
                'fallback': True
            }
        
        results['keywords'] = keyword_extractor.extract_keywords(text, top_n=10)
        results['original_word_count'] = orig_words
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@summarization_bp.route('/api/export/txt', methods=['POST'])
@login_required
def export_txt():
    try:
        data = request.get_json()
        summary_text = data.get('summary_text', '')
        stats = data.get('stats', {})
        content = ExportService.export_txt(summary_text, stats)
        return send_file(
            io.BytesIO(content.encode('utf-8')),
            mimetype='text/plain',
            as_attachment=True,
            download_name='summary.txt'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@summarization_bp.route('/api/export/pdf', methods=['POST'])
@login_required
def export_pdf():
    try:
        data = request.get_json()
        summary_text = data.get('summary_text', '')
        stats = data.get('stats', {})
        content = ExportService.export_pdf(summary_text, stats)
        return send_file(
            io.BytesIO(content),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='summary.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@summarization_bp.route('/api/export/docx', methods=['POST'])
@login_required
def export_docx():
    try:
        data = request.get_json()
        summary_text = data.get('summary_text', '')
        stats = data.get('stats', {})
        content = ExportService.export_docx(summary_text, stats)
        return send_file(
            io.BytesIO(content),
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name='summary.docx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

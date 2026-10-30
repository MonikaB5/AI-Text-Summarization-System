from flask import Flask, render_template, session, redirect, url_for
from config import Config
from models.database import db
from routes.auth_routes import auth_bp
from routes.summarization_routes import summarization_bp
from routes.document_routes import upload_bp
from routes.history_routes import history_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(summarization_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(history_bp)

# Create tables
with app.app_context():
    db.create_all()
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('instance', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@app.route('/summarize')
def summarize_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('summarize.html')

@app.route('/history')
def history_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('history.html')

@app.route('/history/<int:summary_id>')
def summary_detail_page(summary_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('summary_detail.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/health')
def health():
    return {'status': 'healthy', 'service': 'AI Text Summarization System'}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

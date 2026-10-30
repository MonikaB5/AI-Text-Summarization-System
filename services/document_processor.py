import os
import fitz  # PyMuPDF
from docx import Document
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import ipaddress

class DocumentProcessor:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'docx'}
    
    @staticmethod
    def extract_from_txt(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    @staticmethod
    def extract_from_pdf(file_path):
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            if not text.strip():
                return None  # Indicates possible scanned PDF
            return text
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    @staticmethod
    def extract_from_docx(file_path):
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error extracting DOCX: {str(e)}")
    
    @staticmethod
    def is_safe_url(url):
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ['http', 'https']:
                return False
            hostname = parsed.hostname
            if not hostname:
                return False
            # Block localhost and private IPs
            try:
                ip = ipaddress.ip_address(hostname)
                if ip.is_private or ip.is_loopback or ip.is_link_local:
                    return False
            except ValueError:
                pass
            if hostname in ['localhost', '127.0.0.1', '::1']:
                return False
            return True
        except:
            return False
    
    @staticmethod
    def extract_from_url(url):
        if not DocumentProcessor.is_safe_url(url):
            raise Exception("Invalid or unsafe URL")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            if len(response.content) > 5 * 1024 * 1024:
                raise Exception("Content too large")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Try to find main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=['content', 'post', 'article'])
            if main_content:
                text = main_content.get_text()
            else:
                text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            raise Exception(f"Error extracting from URL: {str(e)}")
    
    @staticmethod
    def process_file(file_path, filename):
        ext = filename.rsplit('.', 1)[1].lower()
        if ext == 'txt':
            return DocumentProcessor.extract_from_txt(file_path)
        elif ext == 'pdf':
            result = DocumentProcessor.extract_from_pdf(file_path)
            if result is None:
                raise Exception("This appears to be a scanned PDF. OCR is not configured in this system.")
            return result
        elif ext == 'docx':
            return DocumentProcessor.extract_from_docx(file_path)
        else:
            raise Exception("Unsupported file format")

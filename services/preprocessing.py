import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self, text):
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def tokenize_sentences(self, text):
        text = self.clean_text(text)
        sentences = sent_tokenize(text)
        return [s.strip() for s in sentences if s.strip()]
    
    def tokenize_words(self, text):
        text = self.clean_text(text)
        words = word_tokenize(text.lower())
        return [w for w in words if w.isalnum() and w not in self.stop_words]
    
    def get_word_count(self, text):
        words = word_tokenize(self.clean_text(text))
        return len([w for w in words if w.isalnum()])
    
    def get_sentence_count(self, text):
        sentences = self.tokenize_sentences(text)
        return len(sentences)
    
    def remove_duplicates(self, sentences):
        seen = set()
        unique = []
        for s in sentences:
            normalized = s.lower().strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                unique.append(s)
        return unique

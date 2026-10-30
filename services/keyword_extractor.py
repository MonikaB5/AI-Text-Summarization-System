import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from services.preprocessing import TextPreprocessor

class KeywordExtractor:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
    
    def extract_keywords(self, text, top_n=10):
        if not text or len(text.strip()) < 50:
            return []
        
        sentences = self.preprocessor.tokenize_sentences(text)
        if len(sentences) < 2:
            words = self.preprocessor.tokenize_words(text)
            from collections import Counter
            return [w for w, c in Counter(words).most_common(top_n)]
        
        try:
            vectorizer = TfidfVectorizer(
                max_features=100,
                stop_words='english',
                ngram_range=(1, 2)
            )
            tfidf_matrix = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.sum(axis=0).A1
            word_scores = list(zip(feature_names, scores))
            word_scores.sort(key=lambda x: x[1], reverse=True)
            keywords = [word for word, score in word_scores[:top_n]]
            return keywords
        except Exception as e:
            words = self.preprocessor.tokenize_words(text)
            from collections import Counter
            return [w for w, c in Counter(words).most_common(top_n)]

import networkx as nx
import numpy as np
from services.preprocessing import TextPreprocessor

class TextRankSummarizer:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
    
    def summarize(self, text, ratio=0.3, num_sentences=None):
        if not text or len(text.strip()) < 100:
            sentences = self.preprocessor.tokenize_sentences(text)
            return ' '.join(sentences) if sentences else text
        
        sentences = self.preprocessor.tokenize_sentences(text)
        if len(sentences) <= 3:
            return ' '.join(sentences)
        
        # Calculate number of sentences to extract
        if num_sentences is None:
            num_sentences = max(1, int(len(sentences) * ratio))
        else:
            num_sentences = min(num_sentences, len(sentences))
        
        # Build similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
        
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i == j:
                    continue
                similarity_matrix[i][j] = self.sentence_similarity(sentences[i], sentences[j])
        
        # Apply TextRank
        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph)
        
        # Rank sentences
        ranked_sentences = sorted(((scores[i], s, i) for i, s in enumerate(sentences)), reverse=True)
        
        # Select top sentences and maintain original order
        selected_indices = sorted([ranked_sentences[i][2] for i in range(num_sentences)])
        summary_sentences = [sentences[i] for i in selected_indices]
        
        summary = ' '.join(summary_sentences)
        return summary
    
    def sentence_similarity(self, s1, s2):
        words1 = set(self.preprocessor.tokenize_words(s1))
        words2 = set(self.preprocessor.tokenize_words(s2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0

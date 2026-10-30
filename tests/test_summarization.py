import unittest
from services.extractive_summarizer import TextRankSummarizer
from services.preprocessing import TextPreprocessor

class TestSummarization(unittest.TestCase):
    def setUp(self):
        self.extractive = TextRankSummarizer()
        self.preprocessor = TextPreprocessor()
        self.sample_text = """
        Artificial intelligence is revolutionizing various industries. Machine learning algorithms 
        can analyze vast amounts of data quickly. Natural language processing enables computers 
        to understand human language. Deep learning models have achieved remarkable results. 
        These technologies are being applied in healthcare, finance, and education. AI systems 
        can assist doctors in diagnosis and help students learn more effectively.
        """
    
    def test_extractive_summarization(self):
        summary = self.extractive.summarize(self.sample_text, ratio=0.3)
        self.assertIsNotNone(summary)
        self.assertTrue(len(summary) < len(self.sample_text))
    
    def test_short_text(self):
        short_text = "This is a short text."
        summary = self.extractive.summarize(short_text)
        self.assertIsNotNone(summary)
    
    def test_empty_text(self):
        summary = self.extractive.summarize("")
        self.assertIsNotNone(summary)

if __name__ == '__main__':
    unittest.main()

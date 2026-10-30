import unittest
from services.preprocessing import TextPreprocessor

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.preprocessor = TextPreprocessor()
    
    def test_clean_text(self):
        text = "Hello   World!!!   This is a test."
        cleaned = self.preprocessor.clean_text(text)
        self.assertIn("Hello", cleaned)
    
    def test_tokenize_sentences(self):
        text = "This is first sentence. This is second sentence. This is third."
        sentences = self.preprocessor.tokenize_sentences(text)
        self.assertEqual(len(sentences), 3)
    
    def test_word_count(self):
        text = "Hello world this is a test"
        count = self.preprocessor.get_word_count(text)
        self.assertGreater(count, 0)
    
    def test_empty_text(self):
        sentences = self.preprocessor.tokenize_sentences("")
        self.assertEqual(len(sentences), 0)

if __name__ == '__main__':
    unittest.main()

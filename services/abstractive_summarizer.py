import torch
from transformers import BartForConditionalGeneration, BartTokenizer
from services.preprocessing import TextPreprocessor
import time

class AbstractiveSummarizer:
    _model = None
    _tokenizer = None
    _model_name = None
    
    def __init__(self, model_name='facebook/bart-large-cnn'):
        self.model_name = model_name
        self.preprocessor = TextPreprocessor()
        self.max_input_length = 1024
        self.max_output_length = 142
    
    @classmethod
    def load_model(cls, model_name='facebook/bart-large-cnn'):
        if cls._model is None or cls._model_name != model_name:
            try:
                cls._tokenizer = BartTokenizer.from_pretrained(model_name)
                cls._model = BartForConditionalGeneration.from_pretrained(model_name)
                cls._model_name = model_name
                cls._model.eval()
            except Exception as e:
                raise Exception(f"Failed to load model: {str(e)}")
        return cls._model, cls._tokenizer
    
    def chunk_text(self, text, chunk_size=800, overlap=100):
        sentences = self.preprocessor.tokenize_sentences(text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            if current_length + sentence_words > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                # Keep overlap
                overlap_sentences = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk
                current_chunk = list(overlap_sentences)
                current_length = sum(len(s.split()) for s in current_chunk)
            current_chunk.append(sentence)
            current_length += sentence_words
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def summarize(self, text, ratio=0.3, summary_length='medium'):
        try:
            model, tokenizer = self.load_model(self.model_name)
        except Exception as e:
            raise Exception(f"Model not available: {str(e)}")
        
        # Set output length based on summary_length
        if summary_length == 'short':
            self.max_output_length = 80
        elif summary_length == 'long':
            self.max_output_length = 200
        else:
            self.max_output_length = 142
        
        # Check if text needs chunking
        inputs = tokenizer.encode(text, return_tensors='pt', max_length=self.max_input_length, truncation=True)
        if len(text.split()) > 900:
            # Hierarchical summarization
            chunks = self.chunk_text(text)
            chunk_summaries = []
            for chunk in chunks:
                try:
                    inputs = tokenizer.encode(chunk, return_tensors='pt', max_length=self.max_input_length, truncation=True)
                    with torch.no_grad():
                        summary_ids = model.generate(
                            inputs,
                            max_length=min(self.max_output_length, 120),
                            min_length=30,
                            length_penalty=2.0,
                            num_beams=4,
                            early_stopping=True
                        )
                    chunk_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                    chunk_summaries.append(chunk_summary)
                except Exception:
                    continue
            
            if not chunk_summaries:
                raise Exception("Failed to summarize chunks")
            
            # Summarize combined chunk summaries
            combined = ' '.join(chunk_summaries)
            inputs = tokenizer.encode(combined, return_tensors='pt', max_length=self.max_input_length, truncation=True)
            with torch.no_grad():
                summary_ids = model.generate(
                    inputs,
                    max_length=self.max_output_length,
                    min_length=40,
                    length_penalty=2.0,
                    num_beams=4,
                    early_stopping=True
                )
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
        else:
            inputs = tokenizer.encode(text, return_tensors='pt', max_length=self.max_input_length, truncation=True)
            with torch.no_grad():
                summary_ids = model.generate(
                    inputs,
                    max_length=self.max_output_length,
                    min_length=max(30, int(len(text.split()) * ratio * 0.5)),
                    length_penalty=2.0,
                    num_beams=4,
                    early_stopping=True
                )
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary

from rouge_score import rouge_scorer

class EvaluationService:
    def __init__(self):
        self.scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    def evaluate(self, summary, reference):
        if not summary or not reference:
            return None
        scores = self.scorer.score(reference, summary)
        return {
            'rouge1': {
                'precision': round(scores['rouge1'].precision, 4),
                'recall': round(scores['rouge1'].recall, 4),
                'fmeasure': round(scores['rouge1'].fmeasure, 4)
            },
            'rouge2': {
                'precision': round(scores['rouge2'].precision, 4),
                'recall': round(scores['rouge2'].recall, 4),
                'fmeasure': round(scores['rouge2'].fmeasure, 4)
            },
            'rougeL': {
                'precision': round(scores['rougeL'].precision, 4),
                'recall': round(scores['rougeL'].recall, 4),
                'fmeasure': round(scores['rougeL'].fmeasure, 4)
            },
            'note': 'ROUGE measures text overlap and does not independently prove factual correctness.'
        }
    
    def compare_summaries(self, extractive_summary, abstractive_summary, reference):
        results = {}
        if extractive_summary and reference:
            results['extractive'] = self.evaluate(extractive_summary, reference)
        if abstractive_summary and reference:
            results['abstractive'] = self.evaluate(abstractive_summary, reference)
        return results

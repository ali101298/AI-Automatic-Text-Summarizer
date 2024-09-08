import pickle
import nltk
import pandas as pd
import torch
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from concurrent.futures import ThreadPoolExecutor


class SummarizationPipeline:
    def __init__(self, model_name, tokenizer_name):
        self.tokenizer = PegasusTokenizer.from_pretrained(tokenizer_name)
        self.model = PegasusForConditionalGeneration.from_pretrained(model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)

    def _chunk_text(self, text, max_tokens):
        sentences = nltk.tokenize.sent_tokenize(text)
        current_chunk = []
        chunks = []
        current_len = 0

        for sentence in sentences:
            sentence_len = len(self.tokenizer.encode(sentence))
            if current_len + sentence_len > max_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_len = 0
            current_chunk.append(sentence)
            current_len += sentence_len

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def _prepare_batches(self, texts, max_tokens, batch_size):
        for text in texts:
            chunks = self._chunk_text(text, max_tokens)
            for i in range(0, len(chunks), batch_size):
                yield chunks[i:i + batch_size]

    def _summarize_batch(self, batch):
        batch_tokens = self.tokenizer(batch, truncation=True, padding=True, return_tensors="pt").to(self.device)
        summary_ids = self.model.generate(**batch_tokens, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        return [self.tokenizer.decode(ids, skip_special_tokens=True) for ids in summary_ids]

    def generate_summary(self, texts, max_tokens=512, batch_size=4):
        all_summaries = []
        with ThreadPoolExecutor() as executor:
            for batch in self._prepare_batches(texts, max_tokens, batch_size):
                futures = [executor.submit(self._summarize_batch, b) for b in batch]
                results = [f.result() for f in futures]
                document_summary = " ".join(results)
                all_summaries.append(document_summary)
        return all_summaries
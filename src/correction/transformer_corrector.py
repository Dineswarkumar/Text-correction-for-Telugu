# -*- coding: utf-8 -*-
"""
Neural Seq2Seq Transformer Corrector for Telugu Text.
Supports fine-tuned IndicBART (AI4Bharat) and mT5 (Google).
"""
import torch
import warnings
from typing import List, Union, Optional
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class TransformerCorrector:
    """
    Seq2Seq Transformer text corrector for Telugu.
    Capable of correcting multi-token errors, Sandhi boundary splits,
    and contextual real-word anomalies using fine-tuned IndicBART or mT5.
    """
    
    def __init__(
        self, 
        model_path: str = "ai4bharat/IndicBART", 
        device: Optional[str] = None,
        max_length: int = 128
    ):
        """
        Args:
            model_path: Local directory path or Hugging Face hub model identifier.
            device: 'cuda', 'cpu', or None (auto-detects).
            max_length: Maximum sequence length for input and generation.
        """
        if device:
            self.device = torch.device(device)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            
        self.model_path = model_path
        self.max_length = max_length
        self.model = None
        self.tokenizer = None
        self.is_indicbart = False
        self.is_mt5 = False
        self.te_tag_id = None
        self.task_prefix = ""
        
        self.load_model(model_path)
        
    def load_model(self, path: str):
        """
        Loads the Seq2Seq model weights and tokenizer, configuring language tags or task prefixes.
        """
        self.model_path = path
        path_lower = str(path).lower()
        
        # Identify model family
        if "indicbart" in path_lower:
            self.is_indicbart = True
            self.is_mt5 = False
        elif "mt5" in path_lower or "t5" in path_lower:
            self.is_mt5 = True
            self.is_indicbart = False
            self.task_prefix = "సరిచేయి: "
        else:
            # Default assumption
            self.is_indicbart = True
            self.is_mt5 = False

        try:
            if self.is_indicbart:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    path, 
                    do_lower_case=False, 
                    use_fast=False, 
                    keep_accents=True
                )
                if "<2te>" in self.tokenizer.all_special_tokens:
                    self.te_tag_id = self.tokenizer.convert_tokens_to_ids("<2te>")
            else:
                self.tokenizer = AutoTokenizer.from_pretrained(path)
                
            self.model = AutoModelForSeq2SeqLM.from_pretrained(path).to(self.device)
            self.model.eval()
            
            # Configure decoder language tag for IndicBART
            if self.is_indicbart and self.te_tag_id is not None:
                self.model.config.forced_bos_token_id = self.te_tag_id
                
            self.model.config.max_length = self.max_length
        except Exception as e:
            warnings.warn(f"Failed to load transformer model from '{path}': {e}")
            self.model = None
            self.tokenizer = None
            
    def _format_input(self, text: str) -> str:
        """
        Formats input string with appropriate model-specific tags or prefixes.
        """
        cleaned = text.strip()
        if self.is_indicbart:
            return f"{cleaned} </s> <2te>"
        elif self.is_mt5:
            return f"{self.task_prefix}{cleaned}"
        return cleaned

    def _clean_output(self, decoded_text: str) -> str:
        """
        Strips residual special tokens and language tags.
        """
        text = decoded_text.replace("<2te>", "").replace("</s>", "").replace("<pad>", "").strip()
        return text

    def correct(self, text: str, num_beams: int = 4) -> str:
        """
        Generates corrections using beam search for a single text.
        """
        if not text or not self.model or not self.tokenizer:
            return text
            
        formatted_text = self._format_input(text)
        inputs = self.tokenizer(
            formatted_text, 
            return_tensors="pt", 
            max_length=self.max_length, 
            truncation=True
        ).to(self.device)
        
        gen_kwargs = {
            "max_length": self.max_length,
            "num_beams": num_beams,
            "early_stopping": True
        }
        if self.is_indicbart and self.te_tag_id is not None:
            gen_kwargs["forced_bos_token_id"] = self.te_tag_id
            
        with torch.no_grad():
            outputs = self.model.generate(**inputs, **gen_kwargs)
            
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self._clean_output(decoded)
        
    def batch_correct(self, texts: List[str], batch_size: int = 16, num_beams: int = 4) -> List[str]:
        """
        Generates corrections for a batch of texts with chunked inference.
        """
        if not texts or not self.model or not self.tokenizer:
            return texts
            
        results = []
        for i in range(0, len(texts), batch_size):
            chunk = texts[i:i + batch_size]
            formatted_chunk = [self._format_input(t) for t in chunk]
            
            inputs = self.tokenizer(
                formatted_chunk, 
                return_tensors="pt", 
                padding=True, 
                max_length=self.max_length, 
                truncation=True
            ).to(self.device)
            
            gen_kwargs = {
                "max_length": self.max_length,
                "num_beams": num_beams,
                "early_stopping": True
            }
            if self.is_indicbart and self.te_tag_id is not None:
                gen_kwargs["forced_bos_token_id"] = self.te_tag_id
                
            with torch.no_grad():
                outputs = self.model.generate(**inputs, **gen_kwargs)
                
            decoded_batch = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
            results.extend([self._clean_output(d) for d in decoded_batch])
            
        return results

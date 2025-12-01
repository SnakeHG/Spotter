from huggingface_hub import InferenceClient
import json
import math
import os
import re

class TextEvaluator():
    def __init__(self, api_key=None):
        if api_key == None: 
            api_key = os.getenv("HF_TOKEN")
        self.client = InferenceClient(api_key=api_key)

        self.toxic_pattern = self._compile_json("profanity_list.json")
        self.phish_pattern = self._compile_json("phishing_list.json")

    def _compile_json(self, path):
        with open(path, "r") as f:
            entries = json.load(f)
        pattern = [
            (entry["id"], re.compile(
                r"\b" + entry["match"] + r"\b", re.IGNORECASE), entry)
            for entry in entries
        ]

        return pattern

    def _eval_toxic(self, text):
        result = self.client.text_classification(
            model="unitary/toxic-bert",
            text=text
        )
        score = [float(e.score) for e in result]
        for e in result:
            print(f"TOXIC LABEL: {e.label}, SCORE: {e.score}")

        return score
    
    def _eval_phish(self, text):
        result = self.client.text_classification(
            model="ealvaradob/bert-finetuned-phishing",
            text=text
        )
        for e in result:
            print(f"PHISH LABEL: {e.label}, SCORE: {e.score}")

        if not result:
            return 0.0

        phishing = next((e for e in result if getattr(e, "label", "").lower() == "phishing"),
                result[0])

        # ensure score is a float on the object
        try:
            phishing.score = float(phishing.score)
        except Exception:
            phishing.score = 0.0

        return phishing.score
    
    def _eval_regex(self, text):
        toxic_results = []
        for _, pat, entry in self.toxic_pattern:
            if pat.search(text):
                toxic_results.append(entry)

        phish_results = []
        for _, pat, entry in self.phish_pattern:
            if pat.search(text):
                phish_results.append(entry)

        return len(toxic_results), len(phish_results)
    

    def evaluate(self, text):
        def norm(x):
            l = len(text.split())
            return 1 - math.exp(x / l)
        
        regex = self._eval_regex(text)
        toxic = max(self._eval_toxic(text)) + norm(regex[0])
        phish = norm(regex[1])
        return toxic, phish

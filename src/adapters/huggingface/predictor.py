import requests
from src.config import HUGGINGFACE_API_URL, HUGGINGFACE_TOKEN, MODEL_VERSION
from src.domains.ner.service import merge_tokens
from src.ports.ner.predictor import NERPredictor

class HuggingFaceNERPredictor(NERPredictor):
    def predict(self, tasks: list[dict]) -> list[dict]:
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
            "Content-Type": "application/json",
        }
        response = requests.post(HUGGINGFACE_API_URL, json={"tasks": tasks}, headers=headers)
        hf_predictions = response.json().get("predictions", [])

        predictions = []
        for i, pred in enumerate(hf_predictions):
            if pred:
                task_id = tasks[i].get("id")
                predictions.append(merge_tokens(task_id, pred))
        return predictions

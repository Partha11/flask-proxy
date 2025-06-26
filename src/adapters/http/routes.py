import json
from flask import Blueprint, request, jsonify
from src.adapters.huggingface.predictor import HuggingFaceNERPredictor
from src.config import MODEL_VERSION, LABEL_CONFIG_FILE, LABEL_TAG_FILE

bp = Blueprint("routes", __name__)
predictor = HuggingFaceNERPredictor()


@bp.route("/", methods=["GET"])
def root():
    return jsonify({
        "root": True
    })


@bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })


@bp.route("/setup", methods=["POST"])
def setup():
    with open(LABEL_CONFIG_FILE, "r", encoding="utf-8") as f:
        label_config = f.read()
    with open(LABEL_TAG_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return jsonify({"label_config": label_config, **meta})


@bp.route("/predict", methods=["GET", "POST"])
def predict():
    data = request.json
    tasks = data.get("tasks", [])
    results = predictor.predict(tasks)
    return jsonify({"results": results, "model_version": MODEL_VERSION})

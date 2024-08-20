import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

APP_URL = os.getenv("APP_URL")
APP_PORT = os.getenv("APP_PORT")

MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_VERSION = os.getenv("MODEL_VERSION")

HUGGINGFACE_API_URL = f"{os.getenv("HUGGINGFACE_SPACE_URL")}/{os.getenv('HUGGINGFACE_ENDPOINT')}"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")


def format_prediction(entities):
    score = 0
    result = []
    
    for entity in entities:
        tag = ""
        if "entity" in entity:
            tag = entity["entity"]
            if tag == "O":
                continue
            tag = tag.split("-")[-1]
        elif "entity_group" in entity:
            tag = entity["entity_group"]

        result.append(
            {
                "from_name": "label",
                "to_name": "text",
                "type": "labels",
                "value": {
                    "start": entity["start"],
                    "end": entity["end"],
                    "labels": [tag],
                },
                "score": entity["score"],
            }
        )
        score += entity["score"]
    
    return result, score


@app.route("/", methods=["GET"])
def root():
    # Return the configuration details required by Label Studio
    # currently kept empty as it is not required
    return jsonify({})


@app.route("/health", methods=["GET"])
def health():
    # Return the configuration details required by Label Studio
    # currently kept empty as it is not required
    return jsonify({})


@app.route("/setup", methods=["POST"])
def setup():
    """
    Return the label configuration details required by Label Studio
    This label configuration is used by the frontend to render the labels
    on the labeling tool
    """
    return jsonify(
        {
            "label_config": """
            <View>
                <Labels name="label" toName="text">
                    <Label value="PER" background="#ef5350"/>
                    <Label value="ORG" background="#62a0ea"/>
                    <Label value="LOC" background="#ffa726"/>
                    <Label value="DATE" background="#c061cb"/>
                    <Label value="TIME" background="#26a269"/>
                    <Label value="OBJ" background="#8d6e63"/>
                </Labels>
                <Text name="text" value="$text"/>
            </View>
        """,
            "labels": ["PER", "ORG", "LOC", "DATE", "TIME", "OBJ"],
            "type": "text",
        }
    )


@app.route("/predict", methods=["GET", "POST"])
def predict():
    data = request.json
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.post(HUGGINGFACE_API_URL, json=data, headers=headers)

    hf_predictions = response.json()
    predictions = []

    for i in range(len(hf_predictions.get("predictions", []))):
        data = hf_predictions.get("predictions", [])
        if len(data[i]) == 0:
            continue
        prediction, score = format_prediction(data[i])
        average_score = score / len(data)
        predictions.append(
            {
                "id": data.get("tasks")[i].get("id"),
                "score": average_score,
                "model_version": MODEL_NAME,
                "result": prediction,
            }
        )

    return jsonify({"results": predictions, "model_version": MODEL_VERSION})


if __name__ == "__main__":
    load_dotenv()
    app.run(host=APP_URL, port=APP_PORT)

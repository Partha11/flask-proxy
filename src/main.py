import os
import re
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

APP_URL = os.getenv("APP_URL")
APP_PORT = os.getenv("APP_PORT")

MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_VERSION = os.getenv("MODEL_VERSION")

HUGGINGFACE_API_URL = f"{os.getenv('HUGGINGFACE_SPACE_URL')}/{os.getenv('HUGGINGFACE_ENDPOINT')}"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def merge_tokens(id, ner_output: dict) -> list[dict]:
    predictions = ner_output
    result = []
    
    def get_base_entity(entity: str) -> str:
        """Extract base entity type without B-, I-, E-, S- prefix"""
        match = re.match(r'^[BIES]-(.+)$', entity)
        return match.group(1) if match else entity

    def create_annotation(entity_type: str, text: str, start: int, end: int, score: float) -> dict:
        if not entity_type:
            return None
        clean_entity = re.sub(r'^[BIES]-', '', entity_type)
        return {
            "from_name": "label",
            "to_name": "text",
            "type": "labels",
            "id": f"annotation_{len(result) + 1}",
            "value": {
                "start": start,
                "end": end,
                "text": text,
                "labels": [clean_entity]
            }
        }

    i = 0
    while i < len(predictions):
        # Initialize current entity tracking
        current_entity = get_base_entity(predictions[i]['entity'])
        current_start = predictions[i]['start']
        current_text = []
        max_score = predictions[i]['score']
        last_end = None
        
        # Collect all tokens that belong to the same entity
        while i < len(predictions):
            token = predictions[i]
            next_token = predictions[i + 1] if i + 1 < len(predictions) else None
            
            # Get the base entity type
            token_entity = get_base_entity(token['entity'])
            
            # If entity type changes and not a subword, break
            if token_entity != current_entity and not token['word'].startswith('##'):
                break
                
            # Add current token
            word = token['word'].replace('##', '')
            current_text.append(word)
            max_score = max(max_score, token['score'])
            last_end = token['end']
            
            # Check next token
            if next_token:
                # If next token is not a subword and has different entity type, break
                if (not next_token['word'].startswith('##') and 
                    get_base_entity(next_token['entity']) != current_entity):
                    break
                # If there's a significant gap between tokens, break
                if next_token['start'] - token['end'] > 2:
                    break
            
            i += 1
            
        # Create annotation for the collected tokens
        if current_text:
            result.append(create_annotation(
                current_entity,
                ''.join(current_text),
                current_start,
                last_end,
                max_score
            ))
        
        i += 1

    # Return the final formatted output
    return [{
        "id": id,
        "model_version": "MuRIL 1.0.0",
        "result": result,
        "score": str(predictions[0]['score'])
    }]


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
                    <Label value="GPE" background="#00838F"/>
                    <Label value="LOC" background="#ffa726"/>
                    <Label value="DATE" background="#c061cb"/>
                    <Label value="TIME" background="#26a269"/>
                    <Label value="OBJ" background="#8d6e63"/>
                    <Label value="CW" background="#880E4F"/>
                    <Label value="EVE" background="#7e57c2"/>
                    <Label value="MISC" background="#616161"/>
                </Labels>
                <Text name="text" value="$text"/>
            </View>
        """,
            "labels": ["PER", "ORG", "LOC", "DATE", "TIME", "OBJ", "GPE", "CW", "EVE", "MISC"],
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
    
    print(hf_predictions)

    for i in range(len(hf_predictions.get("predictions", []))):
        pred = hf_predictions.get("predictions", [])
        if len(pred[i]) == 0:
            continue
        prediction = merge_tokens(
            data.get("tasks")[i].get("id"),
            pred[i]
        )
        # average_score = score / len(pred)
        predictions.append(prediction)
    
    # print(predictions)

    return jsonify({"results": predictions, "model_version": MODEL_VERSION})


if __name__ == "__main__":
    load_dotenv()
    app.run(host=APP_URL, port=APP_PORT)

import re
from src.config import MODEL_NAME, MODEL_VERSION


def get_base_entity(entity: str) -> str:
    """
    Extract base entity type without B-, I-, E-, S- prefix
    """
    match = re.match(r"^[BIES]-(.+)$", entity)
    return match.group(1) if match else entity


def create_annotation(
    result, entity_type: str, text: str, start: int, end: int, score: float
) -> dict:
    """
    Create annotation object from model prediction
    """
    if not entity_type:
        return {}
    clean_entity = re.sub(r"^[BIES]-", "", entity_type)
    return {
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
        "id": f"annotation_{len(result) + 1}",
        "value": {"start": start, "end": end, "text": text, "labels": [clean_entity]},
    }


def merge_tokens(id, ner_output: dict) -> list[dict]:
    """
    Merge tokens that belong to the same entity
    """
    predictions = ner_output
    result = []

    i = 0
    while i < len(predictions):
        current_entity = get_base_entity(predictions[i]["entity"])
        current_start = predictions[i]["start"]
        current_text = []
        max_score = predictions[i]["score"]
        last_end = None

        while i < len(predictions):
            token = predictions[i]
            next_token = predictions[i + 1] if i + 1 < len(predictions) else None
            token_entity = get_base_entity(token["entity"])

            if token_entity != current_entity and not token["word"].startswith("##"):
                break

            word = token["word"].replace("##", "")
            current_text.append(word)
            max_score = max(max_score, token["score"])
            last_end = token["end"]

            if next_token:
                if (
                    not next_token["word"].startswith("##")
                    and get_base_entity(next_token["entity"]) != current_entity
                ):
                    break
                if next_token["start"] - token["end"] > 2:
                    break

            i += 1

        if current_text:
            result.append(
                create_annotation(
                    result,
                    current_entity,
                    "".join(current_text),
                    current_start,
                    last_end,
                    max_score,
                )
            )

        i += 1

    return [
        {
            "id": id,
            "model_version": f"{MODEL_NAME} {MODEL_VERSION}",
            "result": result,
            "score": str(predictions[0]["score"]),
        }
    ]

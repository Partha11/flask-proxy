import os
from dotenv import load_dotenv

load_dotenv()

APP_URL = os.getenv("APP_URL")
APP_PORT = os.getenv("APP_PORT")

MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_VERSION = os.getenv("MODEL_VERSION")

HUGGINGFACE_API_URL = f"{os.getenv('HUGGINGFACE_SPACE_URL')}/{os.getenv('HUGGINGFACE_ENDPOINT')}"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

LABEL_CONFIG_FILE = os.getenv("LABEL_CONFIG_FILE")
LABEL_TAG_FILE = os.getenv("LABEL_TAG_FILE")

TEMPERATURE = os.getenv("TEMPERATURE")
MAX_TOKENS = os.getenv("MAX_TOKENS")
TOP_P = os.getenv("TOP_P")
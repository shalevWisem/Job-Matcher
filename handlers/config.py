import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class DataConfig:
    default_model = os.environ.get("SONNET_MODEL")
    db_path = os.environ.get("DB_PATH")
    max_tokens = 50000
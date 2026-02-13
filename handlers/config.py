import os
from  dotenv import load_dotenv

load_dotenv()

class DataConfig:
    default_model = os.getenv("DEFAULT_MODEL")
    db_path = os.getenv("DB_PATH")
    max_tokens = 50000
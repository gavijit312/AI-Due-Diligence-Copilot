from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "DueSense AI"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # API Keys
    OPENAI_API_KEY: str = ""
    DEFAULT_LLM_MODEL: str = "gpt-4o"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Database & Storage
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/duesense_db"
    CHROMA_PERSIST_DIR: Path = Path("./data/chromadb")
    UPLOAD_DIR: Path = Path("./data/uploads")
    TESSERACT_CMD: str = "tesseract"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)


# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5

# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Data Directories
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_FOLDER = BASE_DIR / "data" / "uploads"
VECTOR_DB_PATH = BASE_DIR / "data" / "vector_db"
REPORT_FOLDER = BASE_DIR / "data" / "reports"

# Create directories if they do not exist
for directory in (UPLOAD_FOLDER, VECTOR_DB_PATH, REPORT_FOLDER):
    directory.mkdir(parents=True, exist_ok=True)
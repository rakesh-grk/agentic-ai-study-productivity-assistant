import os
from pathlib import Path
from typing import Optional

def load_dotenv_simple(filepath: str = ".env") -> None:
    """Lightweight, zero-dependency .env loader that parses key=value pairs."""
    env_path = Path(filepath)
    if not env_path.is_file():
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    if key not in os.environ:
                        os.environ[key] = val
    except Exception:
        pass

# Automatically load local .env if present
load_dotenv_simple()

class AppConfig:
    """Application configuration with safe key access and runtime fallback modes."""
    
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    DB_PATH: Path = DATA_DIR / "assistant_memory.db"
    
    # Provider Settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini").lower()
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
    
    MAX_REVISION_ATTEMPTS: int = int(os.getenv("MAX_REVISION_ATTEMPTS", "2"))
    MAX_INPUT_LENGTH: int = 4000
    MAX_FILE_SIZE_BYTES: int = 2 * 1024 * 1024  # 2MB
    
    @classmethod
    def is_api_configured(cls, provider: Optional[str] = None) -> bool:
        prov = (provider or cls.LLM_PROVIDER).lower()
        if prov == "gemini":
            return bool(cls.GEMINI_API_KEY and cls.GEMINI_API_KEY.strip())
        elif prov == "openai":
            return bool(cls.OPENAI_API_KEY and cls.OPENAI_API_KEY.strip())
        elif prov == "anthropic":
            return bool(cls.ANTHROPIC_API_KEY and cls.ANTHROPIC_API_KEY.strip())
        return False

    @classmethod
    def get_masked_key(cls, provider: Optional[str] = None) -> str:
        prov = (provider or cls.LLM_PROVIDER).lower()
        key = ""
        if prov == "gemini":
            key = cls.GEMINI_API_KEY or ""
        elif prov == "openai":
            key = cls.OPENAI_API_KEY or ""
        elif prov == "anthropic":
            key = cls.ANTHROPIC_API_KEY or ""
        
        if not key:
            return "Not Configured"
        if len(key) <= 8:
            return "********"
        return f"{key[:4]}...{key[-4:]}"

# Ensure data directory exists
AppConfig.DATA_DIR.mkdir(parents=True, exist_ok=True)

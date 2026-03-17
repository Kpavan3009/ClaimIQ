from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./claimiq.db"
    ML_MODEL_PATH: str = "models/"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False

    model_config = {
        "env_file": ".env",
    }


settings = Settings()

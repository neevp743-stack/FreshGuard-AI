import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "FreshGuard AI")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "freshguard_super_secret_jwt_key_change_in_production_2026")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "4320")) # 3 days
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./freshguard.db")
    OPEN_FOOD_FACTS_API_URL: str = os.getenv(
        "OPEN_FOOD_FACTS_API_URL", "https://world.openfoodfacts.org/api/v2/product"
    )
    VISION_CONFIDENCE_THRESHOLD: float = float(os.getenv("VISION_CONFIDENCE_THRESHOLD", "0.50"))
    CORS_ORIGINS: list = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000,*").split(",") if origin.strip()]
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Eco-fy"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "tusharjoshi"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "ecofy"
    POSTGRES_PORT: str = "5432"
    
    # Security
    SECRET_KEY: str = "supersecretkey-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60 # 1 month

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.POSTGRES_PASSWORD:
            auth = f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
        else:
            auth = self.POSTGRES_USER
        return f"postgresql+psycopg://{auth}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()

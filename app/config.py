from dotenv import load_dotenv
load_dotenv()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Setting()

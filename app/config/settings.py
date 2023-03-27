from pydantic import BaseSettings


class Settings(BaseSettings):
    database_driver: str = "postgresql+asyncpg"
    database_hostname: str = "0.0.0.0"
    database_port: str = "5432"
    database_password: str = "postgres"
    database_name: str = "postgres"
    database_username: str = "postgres"
    secret_key: str = "MY_SECRET_KEY"
    algorithm: str = "HS256"
    access_token_exp_time: int = 60 * 24 * 7

    class Config:
        env_file = ".env"


settings = Settings()

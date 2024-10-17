from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JWT_KEY: str
    REFRESH_TOKEN_EXPIRES: int
    ACCESS_TOKEN_EXPIRES: int
    ALGORITHM: str

    class Config:
        env_file = "./.env"


settings = Settings()


def get_auth_data():
    return {'key': settings.JWT_KEY, 'algorithm': settings.ALGORITHM}

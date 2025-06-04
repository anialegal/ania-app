import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "empresa")

    DATABASE_URL_EMPRESA: str = os.getenv(
        "DATABASE_URL_EMPRESA",
        "postgresql+asyncpg://ania_user:Anialega125!@ania-db-empresa-prod.cnksmeq80uqz.eu-west-2.rds.amazonaws.com:5432/ania_empresa",
    )

    DATABASE_URL_LEGAL: str = os.getenv(
        "DATABASE_URL_LEGAL",
        "postgresql+asyncpg://ania_user:Anialega125!@ania-db-legal-dev.cnksmeq80uqz.eu-west-2.rds.amazonaws.com:5432/ania_legal_dev",
    )

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")

    @property
    def WRITER_DB_URL(self):
        if self.ENV == "empresa":
            return self.DATABASE_URL_EMPRESA
        elif self.ENV == "legal":
            return self.DATABASE_URL_LEGAL
        else:
            raise ValueError("Entorno no reconocido")

    @property
    def READER_DB_URL(self):
        if self.ENV == "empresa":
            return self.DATABASE_URL_EMPRESA
        elif self.ENV == "legal":
            return self.DATABASE_URL_LEGAL
        else:
            raise ValueError("Entorno no reconocido")


config = Settings()


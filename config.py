import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "empresa")
    SECRET_KEY: str = os.getenv("SECRET_KEY=f93fb8648dc027824b058806bee501a3a2b90de9f767e4bcc71265d5a3178c3f")
    
    if ENV == "empresa":
        DATABASE_URL: str = os.getenv("DATABASE_URL=postgresql://ania_user:Anialegal25!@ania-db-empresa-prod.cnksmeq80uqz.eu-west-2.rds.amazonaws.com:5432/ania_empresa")
    elif ENV == "legal":
        DATABASE_URL: str = os.getenv("DATABASE_URL=postgresql://ania_user:Anialegal25!@ania-db-legal-dev.cnksmeq80uqz.eu-west-2.rds.amazonaws.com:5432/ania_legal_dev")
    else:
        raise ValueError("Entorno no reconocido")

config = Settings()


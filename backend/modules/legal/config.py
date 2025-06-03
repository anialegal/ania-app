import os

env = os.getenv("ENV", "empresa")  # Por defecto usará empresa

if env == "empresa":
    DATABASE_URL = os.getenv("DATABASE_URL_EMPRESA")
elif env == "legal":
    DATABASE_URL = os.getenv("DATABASE_URL_LEGAL")
else:
    raise ValueError("Entorno no reconocido")


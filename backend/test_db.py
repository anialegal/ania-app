import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from modules.shared.core.config import config

ENVIRONMENT = os.getenv("ENVIRONMENT", "legal").lower()

if ENVIRONMENT == "empresa":
    database_url = config.DATABASE_URL_EMPRESA
elif ENVIRONMENT == "legal":
    database_url = config.DATABASE_URL_LEGAL
else:
    raise ValueError(f"Entorno desconocido: {ENVIRONMENT}")

engine = create_async_engine(database_url, echo=True)

async def test_connection():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: None)
            print(f"✅ Conexión con la base de datos [{ENVIRONMENT}] establecida correctamente.")
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos [{ENVIRONMENT}]:")
        print(e)

if __name__ == "__main__":
    asyncio.run(test_connection())


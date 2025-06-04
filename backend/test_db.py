import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from modules.shared.core.config import config

engine = create_async_engine(config.DATABASE_URL, echo=True)

async def test_connection():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: None)
        print("✅ Conexión con la base de datos establecida correctamente.")
    except Exception as e:
        print("❌ Error al conectar con la base de datos:")
        print(e)

if __name__ == "__main__":
    asyncio.run(test_connection())


import asyncio
from app.database.session import engine
from app.models.base import Base  # Must import Base to get metadata
from app.models import user, product  # Explicitly import all models

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.Base.metadata.create_all)
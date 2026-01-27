import os
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.database.core import Base, get_session
from app.api.chat.router import router as chat_router


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:secret@localhost:5433/hitalent_test"
)


@pytest_asyncio.fixture(scope="function")
async def app() -> FastAPI:
    """
    Создает FastAPI приложение с переопределением зависимости db_session.
    Таблицы создаются перед тестом и удаляются после.
    """
    engine = create_async_engine(DATABASE_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app = FastAPI()

    async def override_get_session():
        async with AsyncSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    app.include_router(chat_router)

    yield app

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    """
    Асинхронный HTTP клиент для FastAPI через ASGITransport.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

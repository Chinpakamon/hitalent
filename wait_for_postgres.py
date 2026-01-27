import time
import sqlalchemy

DATABASE_URL = "postgresql+asyncpg://postgres:secret@test-postgres:5432/hitalent_test"

engine = sqlalchemy.create_engine(DATABASE_URL.replace("+asyncpg", ""))

while True:
    try:
        with engine.connect() as conn:
            print("Postgres is ready!")
            break
    except Exception:
        print("Waiting for Postgres...")
        time.sleep(1)

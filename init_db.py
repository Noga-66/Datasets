"""ينشئ الجداول. (للإنتاج: استبدليه بـ Alembic migrations.)"""
from backend.db.models import Base
from backend.db.session import engine

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("tables created")

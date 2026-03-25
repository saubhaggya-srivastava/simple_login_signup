from fastapi import FastAPI

from db.database import engine, Base
from routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Simple Login & Signup API",
    description="A minimal user authentication module with PostgreSQL",
    version="1.0.0",
)

app.include_router(auth_router)


@app.get("/", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}

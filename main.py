from fastapi import FastAPI

import models
from db.database import engine, Base
from routes.auth import router as auth_router
from routes.msl_list import router as msl_list_router
from routes.sku import router as sku_router
from routes.store import router as store_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Simple Login & Signup API",
    description=(
        "FastAPI service for authentication, SKU master, Store master, and MSL list APIs.\n\n"
        "Available docs:\n"
        "- Swagger UI: `/docs`\n"
        "- ReDoc: `/redoc`\n\n"
        "SKU, Store, and MSL APIs support search, exact-match filters, "
        "sorting, pagination, and cascading filter dropdown options."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "Health", "description": "Basic health-check endpoint."},
        {"name": "Authentication", "description": "User signup, login, and password reset APIs."},
        {
            "name": "SKU",
            "description": (
                "SKU master APIs for listing, searching, filtering, sorting, pagination, "
                "and fetching dropdown filter options."
            ),
        },
        {
            "name": "Store",
            "description": (
                "Store master APIs for listing, searching, filtering, sorting, pagination, "
                "and fetching dropdown filter options."
            ),
        },
        {
            "name": "MSL List",
            "description": (
                "MSL list APIs for listing, searching, filtering, sorting, pagination, "
                "and fetching dropdown filter options."
            ),
        },
    ],
)

app.include_router(auth_router)
app.include_router(msl_list_router)
app.include_router(sku_router)
app.include_router(store_router)


@app.get("/", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}

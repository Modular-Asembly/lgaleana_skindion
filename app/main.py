from dotenv import load_dotenv
load_dotenv()  # Must be called before other imports

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.sql_adaptor import engine, Base
from app.routes.shopify_data import router as shopify_data_router
from app.routes.google_ads_data import router as google_ads_data_router
from app.routes.dashboard import router as dashboard_router

def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include all routers
    app.include_router(shopify_data_router)
    app.include_router(google_ads_data_router)
    app.include_router(dashboard_router)

    # Create database tables
    Base.metadata.create_all(bind=engine)

    return app

app = create_app()

import os
from typing import Any, List

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.sql_adaptor import get_session
from app.models.shopify_data import ShopifyData
from app.models.google_ads_data import GoogleAdsData

router = APIRouter()

# Initialize Jinja2 environment pointing to the templates directory.
templates_env = Environment(
    loader=FileSystemLoader("app/templates"),
    autoescape=select_autoescape(["html", "xml"])
)

def fetch_shopify_data(session: Session) -> List[ShopifyData]:
    """Fetch all ShopifyData records."""
    return session.query(ShopifyData).all()

def fetch_google_ads_data(session: Session) -> List[GoogleAdsData]:
    """Fetch all GoogleAdsData records."""
    return session.query(GoogleAdsData).all()

@router.get("/dashboard", response_class=HTMLResponse, tags=["dashboard"])
async def render_dashboard(request: Request, session: Session = Depends(get_session)) -> HTMLResponse:
    """
    Render the dashboard view by querying ShopifyData and GoogleAdsData.
    Uses the 'dashboard.html' Jinja2 template located in app/templates.

    Environment Variables:
    - DASHBOARD_TITLE: Title to display on the dashboard.
    """
    # Get the dashboard title from environment variables, default if not set.
    dashboard_title: str = os.getenv("DASHBOARD_TITLE", "Dashboard")

    # Query both datamodels using the provided session.
    shopify_records = fetch_shopify_data(session)
    google_ads_records = fetch_google_ads_data(session)

    # Render the dashboard template with retrieved data.
    try:
        template = templates_env.get_template("dashboard.html")
    except Exception as template_error:
        raise HTTPException(status_code=500, detail="Template not found.") from template_error

    rendered_page: str = template.render(
        request=request,
        dashboard_title=dashboard_title,
        shopify_data=shopify_records,
        google_ads_data=google_ads_records
    )
    return HTMLResponse(content=rendered_page)

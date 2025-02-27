import os
import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.sql_adaptor import get_session
from app.models.google_ads_data import GoogleAdsData
from app.google_ads_api_client import get_google_ads_data

router = APIRouter()

@router.post("/google-ads-data/pull", tags=["google-ads-data"])
async def pull_data_from_google_ads(session: Session = Depends(get_session)) -> JSONResponse:
    """
    Pull data from Google Ads and store it into the GoogleAdsData table.

    Environment Variables:
    - GOOGLE_ADS_CLIENT_ID: Google Ads client ID.
    - GOOGLE_ADS_CLIENT_SECRET: Google Ads client secret.
    - GOOGLE_ADS_DEVELOPER_TOKEN: Google Ads developer token.
    - GOOGLE_ADS_REFRESH_TOKEN: Google Ads refresh token.

    Dependencies:
    - GoogleAdsData (datamodel)
    - SQL adaptor for database connection
    - google ads api client for fetching data from Google Ads

    Returns:
        A JSONResponse indicating the success of the operation.
    """
    google_ads_client_id: Optional[str] = os.getenv("GOOGLE_ADS_CLIENT_ID")
    google_ads_client_secret: Optional[str] = os.getenv("GOOGLE_ADS_CLIENT_SECRET")
    google_ads_developer_token: Optional[str] = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
    google_ads_refresh_token: Optional[str] = os.getenv("GOOGLE_ADS_REFRESH_TOKEN")
    if not (google_ads_client_id and google_ads_client_secret and google_ads_developer_token and google_ads_refresh_token):
        raise HTTPException(
            status_code=400,
            detail="Missing required Google Ads API configuration."
        )

    logging.info("Starting pull data from Google Ads")

    # Fetch data from Google Ads using the google ads api client module.
    google_ads_response: Dict[str, Any] = get_google_ads_data()
    
    # Assume google_ads_response has a "campaigns" key containing a list of campaigns.
    campaigns = google_ads_response.get("campaigns", [])
    if not isinstance(campaigns, list):
        raise HTTPException(status_code=500, detail="Invalid data format received from Google Ads API client.")

    # Insert each campaign as a record into the GoogleAdsData table.
    for campaign in campaigns:
        # Create a new GoogleAdsData entry.
        # Convert campaign id to string to match the model requirements if not already.
        google_ads_entry = GoogleAdsData(ads_id=str(campaign.get("id")), data=campaign)
        session.add(google_ads_entry)

    # Commit the transaction to persist changes.
    session.commit()

    logging.info("Completed pull data from Google Ads")
    return JSONResponse(
        status_code=200,
        content={"detail": "Google Ads data pulled and stored successfully."}
    )

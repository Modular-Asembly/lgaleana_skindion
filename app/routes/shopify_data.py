import os
import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.sql_adaptor import get_session
from app.models.shopify_data import ShopifyData
from app.shopify_api_client import get_shopify_data

router = APIRouter()


@router.post("/shopify-data/pull", tags=["shopify-data"])
async def pull_sdata_from_shopify(session: Session = Depends(get_session)) -> JSONResponse:
    """
    Pull sdata from Shopify and store it into the ShopifyData table.
    
    Environment Variables:
    - SHOPIFY_API_KEY: API key to access Shopify.
    - SHOPIFY_API_SECRET: API secret for Shopify.
    - SHOPIFY_STORE_URL: The URL of the Shopify store.
    
    Dependencies:
    - ShopifyData (Datamodel)
    - SQL adaptor for database connection
    - shopify api client for fetching data from Shopify
    """
    shopify_api_key: Optional[str] = os.getenv("SHOPIFY_API_KEY")
    shopify_api_secret: Optional[str] = os.getenv("SHOPIFY_API_SECRET")
    shopify_store_url: Optional[str] = os.getenv("SHOPIFY_STORE_URL")
    if not (shopify_api_key and shopify_api_secret and shopify_store_url):
        raise HTTPException(status_code=400, detail="Missing Shopify API configuration.")

    # At this point, we know the environment variables are not None.
    api_key: str = shopify_api_key
    api_secret: str = shopify_api_secret
    store_url: str = shopify_store_url
    
    logging.info("Starting pull sdata from Shopify")

    # Fetch data from Shopify using the shopify API client module.
    shopify_response: Dict[str, Any] = get_shopify_data()

    # Assume shopify_response contains an "orders" key with a list of order dicts.
    orders = shopify_response.get("orders", [])
    if not isinstance(orders, list):
        raise HTTPException(status_code=500, detail="Invalid data format received from Shopify API client.")

    # Insert each order as a record into the ShopifyData table.
    for order in orders:
        # Create a new ShopifyData entry.
        # Convert order id to str in order to match the model requirements.
        shopify_entry = ShopifyData(shopify_id=str(order.get("id")), data=order)
        session.add(shopify_entry)

    # Commit the transaction to persist changes.
    session.commit()

    logging.info("Completed pull sdata from Shopify")
    return JSONResponse(
        status_code=200, 
        content={"detail": "Shopify data pulled and stored successfully."}
    )

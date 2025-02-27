from typing import Any, Dict

def get_google_ads_data() -> Dict[str, Any]:
    """
    Returns dummy Google Ads data mimicking a typical API response.
    The returned dictionary includes basic ads insights.
    """
    dummy_data: Dict[str, Any] = {
        "campaigns": [
            {
                "id": "campaign_1",
                "name": "Campaign One",
                "impressions": 10000,
                "clicks": 300,
                "cost": 150.75,
                "currency": "USD"
            },
            {
                "id": "campaign_2",
                "name": "Campaign Two",
                "impressions": 15000,
                "clicks": 450,
                "cost": 225.50,
                "currency": "USD"
            }
        ],
        "account": {
            "id": "account_12345",
            "name": "Dummy Google Ads Account"
        }
    }
    return dummy_data

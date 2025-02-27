from typing import Any, Dict

def get_shopify_data() -> Dict[str, Any]:
    """
    Returns dummy Shopify data mimicking a typical API response.
    """
    dummy_data: Dict[str, Any] = {
        "orders": [
            {
                "id": 1,
                "status": "paid",
                "total": 100.0,
                "currency": "USD"
            },
            {
                "id": 2,
                "status": "fulfilled",
                "total": 150.0,
                "currency": "USD"
            }
        ],
        "shop": {
            "name": "Dummy Shopify Store",
            "domain": "dummy-shop.myshopify.com"
        }
    }
    return dummy_data

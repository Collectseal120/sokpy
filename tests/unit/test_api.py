import json
from unittest.mock import Mock, patch

from sokpy import SOKAPI, SOKProduct, SOKPricing, SOKStore


def make_response(text, status_code=200):
    response = Mock()
    response.status_code = status_code
    response.text = text
    response.content = text.encode("utf-8")
    response.raise_for_status = Mock()
    return response


def test_get_store_by_id_parses_html():
    store_payload = {
        "props": {
            "pageProps": {
                "store": {
                    "id": "513971200",
                    "slug": "prisma-kaari-kannelmaki",
                    "name": "Prisma Kaari Kannelmäki",
                    "brand": "prisma",
                    "domains": ["www.s-kaupat.fi"],
                    "location": {"address": {"street": {"default": "Kaari 1"}, "postcode": "00420", "postcodeName": {"default": "Helsinki"}}},
                    "weeklyOpeningHours": [{"day": "Mon", "open": "08:00", "close": "22:00"}],
                }
            }
        }
    }
    html = f"<script id=\"__NEXT_DATA__\">{json.dumps(store_payload)}</script>"

    with patch("sokpy.api.requests.get", return_value=make_response(html)):
        api = SOKAPI()
        store = api.get_store_by_id("513971200")

    assert isinstance(store, SOKStore)
    assert store.store_id == "513971200"
    assert store.slug == "prisma-kaari-kannelmaki"
    assert store.brand == "prisma"
    assert store.location == "Kaari 1"


def test_get_product_by_id_parses_html():
    product_payload = {
        "props": {
            "pageProps": {
                "apolloState": {
                    'Product:{"id":"8809220804601","storeId":"513971200"}': {
                        "id": "8809220804601",
                        "sokId": "8809220804601",
                        "name": "Test Product",
                        "price": 4.99,
                        "availability": "in stock",
                        "pricing": {
                            "campaignPrice": 4.49,
                            "lowest30DayPrice": 4.99,
                            "campaignPriceValidUntil": "2026-12-31",
                            "regularPrice": 4.99,
                            "currentPrice": 4.99,
                            "salesUnit": "kg",
                            "comparisonPrice": 9.98,
                            "comparisonUnit": "l",
                            "isApproximatePrice": False,
                            "depositPrice": 0.0,
                            "quantityMultiplier": 1.0,
                        },
                        "basicQuantityUnit": "kg",
                        "comparisonPrice": 9.98,
                        "comparisonUnit": "l",
                        "priceUnit": "kg",
                        "isAgeLimitedByAlcohol": False,
                        "frozen": False,
                        "packagingLabelCodes": [],
                        "brandName": "Test Brand",
                        "packagingLabels": [],
                        "slug": "test-product",
                        "productDetails": {"productImages": {"mainImage": {"urlTemplate": "https://example.com/image.png"}}},
                    }
                }
            }
        }
    }
    html = f"<script id=\"__NEXT_DATA__\">{json.dumps(product_payload)}</script>"

    with patch("sokpy.api.requests.get", return_value=make_response(html)):
        api = SOKAPI()
        product = api.get_product_by_id("8809220804601")

    assert isinstance(product, SOKProduct)
    assert product.product_id == "8809220804601"
    assert product.name == "Test Product"
    assert product.pricing.currentPrice == 4.99
    assert product.urlTemplate == "https://example.com/image.png"


def test_get_stores_by_brand_paginates():
    first_page = {
        "data": {
            "searchStores": {
                "totalCount": 2,
                "stores": [
                    {
                        "id": "111",
                        "slug": "s-market-one",
                        "name": "S-Market One",
                        "brand": "s-market",
                        "domains": ["s-market.fi"],
                        "location": {"address": {"street": {"default": "Street 1"}, "postcode": "00100", "postcodeName": {"default": "Helsinki"}}},
                        "weeklyOpeningHours": [],
                    }
                ],
                "cursor": "cursor-1",
            }
        }
    }
    second_page = {
        "data": {
            "searchStores": {
                "totalCount": 2,
                "stores": [
                    {
                        "id": "222",
                        "slug": "s-market-two",
                        "name": "S-Market Two",
                        "brand": "s-market",
                        "domains": ["s-market.fi"],
                        "location": {"address": {"street": {"default": "Street 2"}, "postcode": "00200", "postcodeName": {"default": "Espoo"}}},
                        "weeklyOpeningHours": [],
                    }
                ],
                "cursor": None,
            }
        }
    }

    api = SOKAPI()
    with patch.object(SOKAPI, "_request", side_effect=[first_page, second_page]):
        stores = api.get_stores_by_brand("S_MARKET")

    assert len(stores) == 2
    assert stores[0].store_id == "111"
    assert stores[1].store_id == "222"


def test_store_get_filtered_products_paginates():
    api = SOKAPI()
    store = SOKStore(
        api=api,
        store_id="513971200",
        slug="prisma-kaari-kannelmaki",
        name="Prisma Kaari Kannelmäki",
        brand="prisma",
        domains=["www.s-kaupat.fi"],
        location="Kaari 1",
        postcode="00420",
        postcodeName="Helsinki",
        weeklyOpeningHours=[{"day": "Mon", "open": "08:00", "close": "22:00"}],
    )

    first_page = {
        "data": {
            "store": {
                "products": {
                    "total": 2,
                    "productListItems": [
                        {"product": {
                            "id": "8809220804601",
                            "sokId": "8809220804601",
                            "name": "Test Product 1",
                            "price": 2.0,
                            "availability": "in stock",
                            "pricing": {
                                "campaignPrice": 1.8,
                                "lowest30DayPrice": 2.0,
                                "campaignPriceValidUntil": "2026-12-31",
                                "regularPrice": 2.0,
                                "currentPrice": 2.0,
                                "salesUnit": "kg",
                                "comparisonPrice": 4.0,
                                "comparisonUnit": "l",
                                "isApproximatePrice": False,
                                "depositPrice": 0.0,
                                "quantityMultiplier": 1.0,
                            },
                            "basicQuantityUnit": "kg",
                            "comparisonPrice": 4.0,
                            "comparisonUnit": "l",
                            "priceUnit": "kg",
                            "isAgeLimitedByAlcohol": False,
                            "frozen": False,
                            "packagingLabelCodes": [],
                            "brandName": "Test Brand",
                            "packagingLabels": [],
                            "slug": "test-product-1",
                        }}
                    ]
                }
            }
        }
    }
    second_page = {
        "data": {
            "store": {
                "products": {
                    "total": 2,
                    "productListItems": [
                        {"product": {
                            "id": "8809220804602",
                            "sokId": "8809220804602",
                            "name": "Test Product 2",
                            "price": 3.0,
                            "availability": "in stock",
                            "pricing": {
                                "campaignPrice": 2.5,
                                "lowest30DayPrice": 3.0,
                                "campaignPriceValidUntil": "2026-12-31",
                                "regularPrice": 3.0,
                                "currentPrice": 3.0,
                                "salesUnit": "kg",
                                "comparisonPrice": 6.0,
                                "comparisonUnit": "l",
                                "isApproximatePrice": False,
                                "depositPrice": 0.0,
                                "quantityMultiplier": 1.0,
                            },
                            "basicQuantityUnit": "kg",
                            "comparisonPrice": 6.0,
                            "comparisonUnit": "l",
                            "priceUnit": "kg",
                            "isAgeLimitedByAlcohol": False,
                            "frozen": False,
                            "packagingLabelCodes": [],
                            "brandName": "Test Brand",
                            "packagingLabels": [],
                            "slug": "test-product-2",
                        }}
                    ]
                }
            }
        }
    }

    with patch.object(api, "_request", side_effect=[first_page, second_page]):
        products = store.get_filtered_products("grillaus", limit=1)

    assert len(products) == 2
    assert products[0].product_id == "8809220804601"
    assert products[1].product_id == "8809220804602"

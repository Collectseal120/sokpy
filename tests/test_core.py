import json

from sokpy import SOKAPI, SOKPricing, SOKProduct, SOKStore


def test_sokpricing_to_dict_and_json():
    pricing = SOKPricing(
        campaignPrice=1.0,
        lowest30DayPrice=0.9,
        campaignPriceValidUntil="2026-12-31",
        regularPrice=1.2,
        currentPrice=1.0,
        salesUnit="kg",
        comparisonPrice=2.5,
        comparisonUnit="l",
        isApproximatePrice=False,
        depositPrice=0.1,
        quantityMultiplier=1.0,
    )

    expected = {
        "campaignPrice": 1.0,
        "lowest30DayPrice": 0.9,
        "campaignPriceValidUntil": "2026-12-31",
        "regularPrice": 1.2,
        "currentPrice": 1.0,
        "salesUnit": "kg",
        "comparisonPrice": 2.5,
        "comparisonUnit": "l",
        "isApproximatePrice": False,
        "depositPrice": 0.1,
        "quantityMultiplier": 1.0,
    }

    assert pricing.to_dict() == expected
    assert json.loads(pricing.to_json()) == expected


def test_sokproduct_to_dict_and_json():
    pricing = SOKPricing(
        campaignPrice=1.0,
        lowest30DayPrice=0.9,
        campaignPriceValidUntil="2026-12-31",
        regularPrice=1.2,
        currentPrice=1.0,
        salesUnit="kg",
        comparisonPrice=2.5,
        comparisonUnit="l",
        isApproximatePrice=False,
        depositPrice=0.1,
        quantityMultiplier=1.0,
    )

    product = SOKProduct(
        product_id="product-123",
        sokId="sok-123",
        name="Test Product",
        price=3.5,
        availability="in stock",
        pricing=pricing,
        basicQuantityUnit="kg",
        comparisonPrice=2.5,
        comparisonUnit="l",
        priceUnit="kg",
        isAgeLimitedByAlcohol=False,
        frozen=False,
        packagingLabelCodes=["label1", "label2"],
        brandName="Test Brand",
        packagingLabels=["labelA"],
        slug="test-product",
        urlTemplate="https://example.com/image.png",
    )

    expected = {
        "product_id": "product-123",
        "sokId": "sok-123",
        "name": "Test Product",
        "price": 3.5,
        "availability": "in stock",
        "pricing": pricing.to_dict(),
        "basicQuantityUnit": "kg",
        "comparisonPrice": 2.5,
        "comparisonUnit": "l",
        "priceUnit": "kg",
        "isAgeLimitedByAlcohol": False,
        "frozen": False,
        "packagingLabelCodes": ["label1", "label2"],
        "brandName": "Test Brand",
        "packagingLabels": ["labelA"],
        "slug": "test-product",
        "urlTemplate": "https://example.com/image.png",
    }

    assert product.to_dict() == expected
    assert json.loads(product.to_json()) == expected


def test_sokstore_to_dict_and_json():
    api = SOKAPI()
    store = SOKStore(
        api=api,
        store_id="store-123",
        slug="test-store",
        name="Test Store",
        brand="S-Market",
        domains=["www.s-market.fi"],
        location="Test Street 1",
        postcode="00100",
        postcodeName="Helsinki",
        weeklyOpeningHours=[{"day": "Mon", "open": "08:00", "close": "22:00"}],
    )

    expected = {
        "store_id": "store-123",
        "slug": "test-store",
        "name": "Test Store",
        "brand": "S-Market",
        "domains": ["www.s-market.fi"],
        "location": "Test Street 1",
        "postcode": "00100",
        "postcodeName": "Helsinki",
        "weeklyOpeningHours": [{"day": "Mon", "open": "08:00", "close": "22:00"}],
        "categories": {},
    }

    assert store.to_dict() == expected
    assert json.loads(store.to_json()) == expected

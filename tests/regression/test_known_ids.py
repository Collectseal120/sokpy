import os

import pytest

from sokpy import SOKAPI

LIVE_TESTS = os.getenv("RUN_LIVE_TESTS") == "1"
STORE_ID = "513971200"
PRODUCT_ID = "8809220804601"


@pytest.mark.regression
def test_regression_store_id_remains_valid():
    if not LIVE_TESTS:
        pytest.skip("Set RUN_LIVE_TESTS=1 to run live regression tests")

    api = SOKAPI()
    store = api.get_store_by_id(STORE_ID)

    assert store.store_id == STORE_ID
    assert "Prisma" in store.name
    assert store.slug == "prisma-kaari-kannelmaki"


@pytest.mark.regression
def test_regression_product_id_remains_valid():
    if not LIVE_TESTS:
        pytest.skip("Set RUN_LIVE_TESTS=1 to run live regression tests")

    api = SOKAPI()
    product = api.get_product_by_id(PRODUCT_ID)

    assert product.product_id == PRODUCT_ID
    assert product.name
    assert product.pricing.currentPrice > 0

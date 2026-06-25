import os

import pytest

from sokpy import SOKAPI, sok_stores

LIVE_TESTS = os.getenv("RUN_LIVE_TESTS") == "1"


@pytest.mark.integration
def test_get_stores_by_brand_live():
    if not LIVE_TESTS:
        pytest.skip("Set RUN_LIVE_TESTS=1 to run live integration tests")

    api = SOKAPI()
    stores = api.get_stores_by_brand("S_MARKET")

    assert stores
    assert all(hasattr(store, "store_id") for store in stores)


@pytest.mark.integration
def test_get_store_by_id_live():
    if not LIVE_TESTS:
        pytest.skip("Set RUN_LIVE_TESTS=1 to run live integration tests")

    api = SOKAPI()
    store = api.get_store_by_id("513971200")

    assert store.store_id == "513971200"
    assert "Prisma" in store.name


@pytest.mark.integration
def test_get_product_by_id_live():
    if not LIVE_TESTS:
        pytest.skip("Set RUN_LIVE_TESTS=1 to run live integration tests")

    api = SOKAPI()
    product = api.get_product_by_id("8809220804601")

    assert product.product_id == "8809220804601"
    assert product.name
    assert product.pricing.currentPrice is not None


@pytest.mark.integration
def test_load_categories_and_fetch_products_live():
    if not LIVE_TESTS:
        pytest.skip("Set RUN_LIVE_TESTS=1 to run live integration tests")

    api = SOKAPI()
    store = api.get_store_by_id(sok_stores.DEFAULT_STORE_ID)
    store.categories._load_root_categories()

    assert store.categories.root
    assert len(store.categories.root) > 0

    slugs = list(store.categories.root)[:3]
    for category_slug in slugs:
        products = store.get_filtered_products(category_slug, limit=10)
        assert products
        assert all(hasattr(product, "product_id") for product in products)


@pytest.mark.integration
def test_category_products_method_live():
    if not LIVE_TESTS:
        pytest.skip("Set RUN_LIVE_TESTS=1 to run live integration tests")

    api = SOKAPI()
    store = api.get_store_by_id(sok_stores.DEFAULT_STORE_ID)
    store.categories._load_root_categories()

    first_category = next(iter(store.categories.root.values()))
    products = first_category.products(limit=10)

    assert products
    assert all(hasattr(product, "product_id") for product in products)


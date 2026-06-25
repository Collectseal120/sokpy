import json
from unittest.mock import Mock, patch

import pytest

from sokpy import SOKAPI
from sokpy.categories import SOKCategories, SOKCategory
from sokpy.stores import SOKStore


def make_response(text, status_code=200):
    response = Mock()
    response.status_code = status_code
    response.text = text
    response.content = text.encode("utf-8")
    response.raise_for_status = Mock()
    return response


def test_load_root_categories_parses_html():
    html = (
        '<div class="item-name"><a href="/tuotteet/hedelmat-ja-vihannekset">Hedelmät ja vihannekset</a></div>'
        '<div class="item-name"><a href="/tuotteet/liha-ja-kasviproteiinit">Liha ja kasviproteiinit</a></div>'
    )

    with patch("sokpy.categories.requests.get", return_value=make_response(html)):
        categories = SOKCategories(store=Mock())
        categories._load_root_categories()


    assert "hedelmat-ja-vihannekset" in categories.root
    assert "liha-ja-kasviproteiinit" in categories.root


def test_category_products_calls_store_filter():
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
    category = SOKCategory(store, "hedelmat-ja-vihannekset")

    expected_products = [Mock()]
    with patch.object(store, "get_filtered_products", return_value=expected_products) as mocked_filter:
        result = category.products(limit=5)

    mocked_filter.assert_called_once_with("hedelmat-ja-vihannekset", 5)
    assert result is expected_products

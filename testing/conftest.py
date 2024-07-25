import pytest
import json

import pytest

from scraper import app, cache, get_product_details


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    app.config["CACHE_TYPE"] = "simple"  # Use simple cache for testing
    cache.clear()
    return app.test_client()


@pytest.fixture()
def runner():
    return app.test_cli_runner()


@pytest.fixture
def json_data():
    with open("./testing/womens_leggings.json") as f:
        data = json.load(f)
    return data

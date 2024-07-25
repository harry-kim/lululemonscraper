from scraper import get_product_details


def test_get_product_details_method(json_data):
    data = get_product_details("mock_url", json_data)
    assert data["url"] == "mock_url"
    assert len(data["records"]) == 12
    assert data["records"][0]["displayName"] == ['Wunder Train High-Rise Tight 28"']
    assert data["records"][0]["url"] == [
        "/p/womens-leggings/Wunder-Train-HR-Tight-28/_/prod10440282"
    ]


def test_malformed_json():
    malformed_json = {
        "contents": [
            {"mainContent": [{"contents": [{"records": [{"attributes": {}}]}]}]}
        ]
    }
    mock_url = "http://example.com/product.json"
    expected_result = {
        "url": mock_url,
        "records": [
            {
                "activities": None,
                "available": None,
                "category": None,
                "colors": None,
                "displayName": None,
                "images": None,
                "price": None,
                "sizes": None,
                "title": None,
                "url": None,
            },
        ],
    }
    result = get_product_details(mock_url, malformed_json)
    assert result == expected_result


def test_missing_main_content():
    missing_main_content_json = {"contents": [{}]}
    mock_url = "http://example.com/product.json"
    expected_result = {"url": mock_url, "records": []}
    result = get_product_details(mock_url, missing_main_content_json)
    assert result == expected_result


def test_empty_json():
    empty_json = {}
    mock_url = "http://example.com/product.json"
    expected_result = {"url": mock_url, "records": []}
    result = get_product_details(mock_url, empty_json)
    assert result == expected_result

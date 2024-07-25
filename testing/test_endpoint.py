import mock


@mock.patch("scraper.requests.get")
def test_product_details(mock_get, client, json_data):
    mock_get.return_value.json.return_value = json_data

    response = client.post("/productDetails", json={"urls": ["mock_leggings_url"]})
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["product_details"]) == 1
    assert data["product_details"][0]["url"] == "mock_leggings_url"
    assert len(data["product_details"][0]["records"]) == 12
    assert data["product_details"][0]["records"][0]["displayName"] == [
        'Wunder Train High-Rise Tight 28"'
    ]
    assert data["product_details"][0]["records"][0]["url"] == [
        "/p/womens-leggings/Wunder-Train-HR-Tight-28/_/prod10440282"
    ]


def test_product_details_without_urls(client):
    response = client.post("/productDetails", json={"urls": []})
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["product_details"]) == 0


def test_product_details_invalid_payload(client):
    response = client.post("/productDetails", json={})
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["product_details"]) == 0


def test_product_details_requires_json_payload(client):
    response = client.post("/productDetails")

    assert response.status_code == 415

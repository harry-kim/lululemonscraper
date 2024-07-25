import logging
import requests_mock


def test_caching(client, json_data, caplog):
    url = "http://example.com/product.json"

    with requests_mock.Mocker() as m:
        m.get(url, json=json_data)

        # First request should fetch data from the external URL
        with caplog.at_level(logging.INFO):
            response = client.post("/productDetails", json={"urls": [url]})
            assert response.status_code == 200
            assert "Fetching data for URL" in caplog.text
            first_result = response.get_json()

        # Clear the log
        caplog.clear()

        # Second request should hit the cache
        with caplog.at_level(logging.INFO):
            response = client.post("/productDetails", json={"urls": [url]})
            assert response.status_code == 200
            assert "Fetching data for URL" not in caplog.text
            second_result = response.get_json()

        # Ensure that the cached result matches the first result
        assert first_result == second_result


def test_no_cache(client, json_data):
    url = "http://example.com/product.json"

    with requests_mock.Mocker() as m:
        # First request should fetch data from the external URL
        m.get(url, json=json_data)

        # First call to endpoint
        response = client.post("/productDetails", json={"urls": [url]})
        assert response.status_code == 200
        first_result = response.get_json()

        # Change the response for the second call
        updated_json_data = json_data.copy()
        updated_json_data["contents"][0]["mainContent"][0]["contents"][0]["records"][0][
            "attributes"
        ]["product.displayName"] = "Updated Product"
        m.get(url, json=updated_json_data)

        # Second call should still hit the cache and return the original response
        response = client.post("/productDetails", json={"urls": [url]})
        assert response.status_code == 200
        second_result = response.get_json()

        # Ensure that the cached result matches the first result and not the updated one
        assert first_result == second_result

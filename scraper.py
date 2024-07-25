import json
import logging
import awsgi2
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_caching import Cache
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__, static_folder="static")

app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DIR"] = "cache-directory"
app.config["CACHE_DEFAULT_TIMEOUT"] = 600  # Cache for 10 minutes
cache = Cache(app)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Lululemon Scraper"},
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/productDetails")
def product_details():
    urls = request.json.get("urls", [])
    product_details = []

    for url in urls:
        json_data = get_cached_json(url)
        product_detail = get_product_details(url, json_data)
        product_details.append(product_detail)

    return jsonify({"product_details": product_details})


@cache.memoize()
def get_cached_json(url):
    logger.info(f"Fetching data for URL: {url}")
    response = requests.get(url)
    return response.json()


def get_product_details(url, json_data):
    product_detail = {"url": url, "records": []}

    for content in json_data.get("contents", []):
        for main_content in content.get("mainContent", []):
            for main_content_content in main_content.get("contents", []):
                for record in main_content_content.get("records", []):
                    attributes = record.get("attributes", {})
                    product_detail_record = {
                        "displayName": attributes.get("product.displayName"),
                        "title": attributes.get("product.title"),
                        "price": attributes.get("product.price"),
                        "images": attributes.get("product.sku.skuImages"),
                        "sizes": attributes.get("product.allAvailableSizes"),
                        "colors": attributes.get("colorCodeDesc"),
                        "activities": attributes.get("product.activity"),
                        "available": attributes.get("sku.available"),
                        "url": attributes.get("product.pdpURL"),
                        "category": attributes.get(
                            "product.parentCategory.displayName"
                        ),
                    }
                    product_detail["records"].append(product_detail_record)

    return product_detail


if __name__ == "__main__":
    app.run(debug=True)


def lambda_handler(event, context):
    logger.info("Received event: %s", event)

    try:
        return awsgi2.response(app, event, context)
    except Exception as e:
        logger.error("Error processing request: %s", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }

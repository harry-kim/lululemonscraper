
## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/harry-kim/lululemonscraper.git
    cd lululemonscraper
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run the Flask application locally:
    ```bash
    python scraper.py
    ```

## API Documentation

### Endpoint
- `POST /productDetails`

### Request
- `Content-Type: application/json`
- Body:
    ```json
    {
      "urls": [
        "https://shop.lululemon.com/c/womens-leggings/_/N-8r6?format=json",
        "https://shop.lululemon.com/c/accessories/_/N-1z0xcmkZ1z0xl44Z8ok?format=json"
      ]
    }
    ```

### Response
- `Content-Type: application/json`
- Body:
    ```json
    {
      "product_details": [
        {
          "url": "https://shop.lululemon.com/c/womens-leggings/_/N-8r6?format=json",
          "records": [
            {
              "displayName": "Product Name",
              "title": "Product Title",
              "price": 100,
              "images": ["image1.jpg", "image2.jpg"],
              "sizes": ["S", "M", "L"],
              "colors": "Black",
              "activities": "Yoga",
              "available": true,
              "url": "https://shop.lululemon.com/p/product-url",
              "category": "Women's Leggings"
            }
          ]
        },
        ...
      ]
    }
    ```

### Example cURL Request

```bash
curl -X POST http://127.0.0.1/productDetails \
     -H "Content-Type: application/json" \
     -d '{
           "urls": [
             "https://shop.lululemon.com/c/womens-leggings/_/N-8r6?format=json",
             "https://shop.lululemon.com/c/accessories/_/N-1z0xcmkZ1z0xl44Z8ok?format=json"
           ]
         }'
```

## Swagger Documentation

You can access the Swagger documentation for the API to explore and test the endpoints.

- **Local URL**: [http://127.0.0.1:5000/swagger](http://127.0.0.1:5000/swagger)

## Caching Mechanism

The API uses `Flask-Caching` to reduce repeated requests to the Lululemon API. The defaults are set to use an in-memory cache with a timeout of 10 minutes.
While `SimpleCache` is suitable for development and testing, for production environments, a persistent caching solution like Amazon ElastiCache or DynamoDB is recommended to ensure cache persistence across serverless function invocations.

### Configuring Cache
In `scraper.py`, the cache is set up as follows:

```python
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 600
cache = Cache(app)
```

## Deployment

### Using AWS SAM

1. **Build the SAM application:**
    ```bash
    sam build
    ```

2. **Deploy the SAM application:**
    ```bash
    sam deploy --guided
    ```

   Follow the prompts to configure your stack, including specifying a stack name, AWS region, and S3 bucket for deployment artifacts.

## Unit Tests

Unit tests are included to ensure the correctness of the implementation. To run the tests:

```bash
pytest
```
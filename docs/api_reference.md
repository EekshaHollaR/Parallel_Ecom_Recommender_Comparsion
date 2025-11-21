# API Reference

Base URL: `http://localhost:5000`

## Recommendations

### Get Recommendations
Fetch top-N product recommendations for a specific user.

-   **URL**: `/recommendations`
-   **Method**: `GET`
-   **Query Parameters**:
    -   `user_id` (int, required): The ID of the user to generate recommendations for.
    -   `n` (int, optional): Number of recommendations to return. Default: 10.
    -   `async` (bool, optional): If `true`, runs in background. Default: `false`.

#### Success Response (Sync)
```json
{
  "status": "success",
  "data": {
    "user_id": 123,
    "recommendations": [
      { "item_id": 456, "score": 4.95 },
      { "item_id": 789, "score": 4.82 }
    ]
  },
  "latency_ms": 45.2
}
```

#### Success Response (Async)
```json
{
  "status": "accepted",
  "job_id": "uuid-string",
  "message": "Recommendation task started"
}
```

## Price Comparison

### Compare Prices
Scrape and compare prices for a product across multiple sites.

-   **URL**: `/compare_price`
-   **Method**: `GET`
-   **Query Parameters**:
    -   `product` (string, required): Name of the product to search for.
    -   `async` (bool, optional): If `true`, runs in background. Default: `false`.

#### Success Response
```json
{
  "status": "success",
  "data": {
    "product": "Sony WH-1000XM5",
    "results": [
      {
        "site": "Amazon",
        "price": 348.00,
        "product_url": "https://amazon.com/...",
        "source": "cache"
      },
      {
        "site": "eBay",
        "price": 320.50,
        "product_url": "https://ebay.com/...",
        "source": "scraped"
      }
    ],
    "total_latency_ms": 1200.5
  }
}
```

## Tasks

### Get Task Status
Check the status and result of an asynchronous background job.

-   **URL**: `/tasks/<job_id>`
-   **Method**: `GET`

#### Response (Pending)
```json
{
  "status": "success",
  "data": {
    "job_id": "uuid-string",
    "job_status": "queued"
  }
}
```

#### Response (Finished)
```json
{
  "status": "success",
  "data": {
    "job_id": "uuid-string",
    "job_status": "finished",
    "result": { ... } // Result from recommendation or scraper
  }
}
```

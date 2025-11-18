# Carbon Footprint Tracker API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, no authentication is required. A `user_id` parameter is used to separate user data.

## Endpoints

### Health Check

#### GET `/`
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "app": "Carbon Footprint Tracker",
  "version": "1.0.0"
}
```

---

### Transactions

#### POST `/api/transactions`
Create a single transaction manually.

**Request Body:**
```json
{
  "description": "Starbucks Coffee",
  "amount": 6.75,
  "date": "2024-01-15",
  "user_id": "default_user"
}
```

**Response:**
```json
{
  "id": 1,
  "description": "Starbucks Coffee",
  "amount": 6.75,
  "category": "dining",
  "carbon_kg": 3.38,
  "confidence_score": 0.9,
  "date": "2024-01-15T00:00:00"
}
```

#### GET `/api/transactions`
Get all transactions for a user.

**Query Parameters:**
- `user_id` (string): User identifier (default: "default_user")
- `limit` (integer): Maximum number of transactions (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "description": "Starbucks Coffee",
    "amount": 6.75,
    "category": "dining",
    "carbon_kg": 3.38,
    "confidence_score": 0.9,
    "date": "2024-01-15T00:00:00"
  }
]
```

#### POST `/api/transactions/upload`
Upload transactions from a CSV file.

**Form Data:**
- `file` (file): CSV file with transaction data
- `user_id` (string): User identifier

**CSV Format:**
```csv
date,description,amount
2024-01-15,Whole Foods Market,87.50
2024-01-16,Shell Gas Station,45.00
```

**Response:**
```json
[
  {
    "id": 1,
    "description": "Whole Foods Market",
    "amount": 87.50,
    "category": "food_plant",
    "carbon_kg": 17.50,
    "confidence_score": 0.8,
    "date": "2024-01-15T00:00:00"
  }
]
```

---

### Dashboard

#### GET `/api/dashboard`
Get dashboard statistics and analytics.

**Query Parameters:**
- `user_id` (string): User identifier (default: "default_user")

**Response:**
```json
{
  "total_carbon_kg": 1234.56,
  "monthly_carbon_kg": 456.78,
  "transaction_count": 45,
  "category_breakdown": {
    "food_meat": 234.50,
    "transportation_air": 875.00,
    "energy": 125.06
  },
  "top_category": "transportation_air",
  "comparison_to_average": {
    "user_monthly_kg": 456.78,
    "average_monthly_kg": 1333.0,
    "difference_kg": -876.22,
    "percentage": 34.27,
    "status": "below_average"
  }
}
```

---

### Suggestions

#### GET `/api/suggestions`
Get personalized carbon reduction suggestions.

**Query Parameters:**
- `user_id` (string): User identifier (default: "default_user")

**Response:**
```json
[
  {
    "suggestion": "Try 'Meatless Mondays' - replace one meat meal per week with plant-based alternatives",
    "reduction_kg": 35.18,
    "difficulty": "easy",
    "category": "food"
  },
  {
    "suggestion": "For trips under 500 miles, consider train or bus travel instead of flying",
    "reduction_kg": 700.00,
    "difficulty": "medium",
    "category": "transportation"
  }
]
```

---

### Sample Data

#### POST `/api/sample-data`
Load sample transaction data for testing/demo.

**Query Parameters:**
- `user_id` (string): User identifier (default: "default_user")

**Response:**
```json
{
  "message": "Loaded 10 sample transactions",
  "transactions": [
    {
      "description": "Whole Foods Market - Organic Groceries",
      "carbon_kg": 17.50
    }
  ]
}
```

---

## Categories

The following categories are supported for transaction classification:

| Category | Description | Avg CO₂ per $ |
|----------|-------------|---------------|
| `food_meat` | Meat and animal products | 0.8 kg |
| `food_plant` | Plant-based foods | 0.2 kg |
| `transportation_air` | Air travel | 2.5 kg |
| `transportation_car` | Car fuel | 1.2 kg |
| `transportation_public` | Public transit | 0.3 kg |
| `energy` | Utilities and energy | 0.9 kg |
| `retail_clothing` | Clothing and fashion | 0.6 kg |
| `retail_electronics` | Electronics | 0.7 kg |
| `retail_general` | General retail | 0.4 kg |
| `services` | Digital services | 0.1 kg |
| `dining` | Restaurants | 0.5 kg |
| `other` | Uncategorized | 0.3 kg |

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error processing file: Invalid CSV format"
}
```

### 404 Not Found
```json
{
  "detail": "Transaction not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Interactive Documentation

Visit http://localhost:8000/docs for interactive API documentation with Swagger UI.

Visit http://localhost:8000/redoc for alternative documentation with ReDoc.

---

## Examples

### cURL Examples

**Create a transaction:**
```bash
curl -X POST "http://localhost:8000/api/transactions" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Whole Foods Market",
    "amount": 87.50,
    "user_id": "default_user"
  }'
```

**Get dashboard:**
```bash
curl "http://localhost:8000/api/dashboard?user_id=default_user"
```

**Upload CSV:**
```bash
curl -X POST "http://localhost:8000/api/transactions/upload" \
  -F "file=@sample_data.csv" \
  -F "user_id=default_user"
```

### Python Examples

```python
import requests

# Create a transaction
response = requests.post(
    "http://localhost:8000/api/transactions",
    json={
        "description": "Starbucks Coffee",
        "amount": 6.75,
        "user_id": "my_user"
    }
)
print(response.json())

# Get dashboard stats
response = requests.get(
    "http://localhost:8000/api/dashboard",
    params={"user_id": "my_user"}
)
stats = response.json()
print(f"Total carbon: {stats['total_carbon_kg']} kg CO₂")

# Upload CSV
with open("transactions.csv", "rb") as f:
    files = {"file": f}
    data = {"user_id": "my_user"}
    response = requests.post(
        "http://localhost:8000/api/transactions/upload",
        files=files,
        data=data
    )
print(response.json())
```

### JavaScript Examples

```javascript
// Create a transaction
fetch('http://localhost:8000/api/transactions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    description: 'Starbucks Coffee',
    amount: 6.75,
    user_id: 'my_user'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));

// Get dashboard
fetch('http://localhost:8000/api/dashboard?user_id=my_user')
  .then(response => response.json())
  .then(stats => console.log(`Total carbon: ${stats.total_carbon_kg} kg CO₂`));
```

---

## Rate Limiting

Currently, no rate limiting is implemented. This may be added in future versions.

## Versioning

Current API version: `1.0.0`

Future versions will be prefixed with the version number (e.g., `/api/v2/transactions`).

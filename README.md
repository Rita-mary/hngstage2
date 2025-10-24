# 🌍 HNG Stage 2 — Country Currency & Exchange API

A RESTful API built with **Django** and **Django REST Framework** for managing country, currency, and exchange rate data.

This project fetches data from public APIs, stores them in a MySQL database, computes estimated GDPs, and exposes endpoints for CRUD operations, filters, and analytics.

---

## 🚀 Features

✅ Fetch all countries and exchange rates from external APIs  
✅ Store or update records in MySQL (caching mechanism)  
✅ Compute `estimated_gdp = population × random(1000–2000) ÷ exchange_rate`  
✅ Filter and sort by region, currency, or GDP  
✅ Generate and serve a summary image (top 5 GDP countries)  
✅ Swagger / OpenAPI documentation with **drf-spectacular**  
✅ Proper error handling with consistent JSON responses  

---

## 🧩 Tech Stack

- **Backend Framework:** Django 5 + Django REST Framework  
- **Database:** MySQL 8  
- **Documentation:** drf-spectacular  
- **Image Generation:** Pillow  
- **Environment Variables:** python-dotenv  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Rita-mary/hngstage2.git
cd hngstage2
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv .venv
# On Linux/Mac
source venv/Scripts/activate
# On Windows
.venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```


### 4️⃣ Create a `.env` file
At the root of your project (`hngstage2/.env`):

```
DB_NAME=hngstage2
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=3306
```

*(You can change credentials as needed.)*

### 5️⃣ Configure Database
Make sure MySQL is running and create the database:

```sql
CREATE DATABASE hngstage2;
```

Then apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Run the development server
```bash
python manage.py runserver
```

Server starts at:  
➡️ **http://127.0.0.1:8000/**

---

## 🌐 API Endpoints

All endpoints return **JSON** responses.

| Method | Endpoint | Description |
|---------|-----------|-------------|
| `POST` | `/api/countries/refresh` | Fetches countries and exchange rates, caches them in DB |
| `GET` | `/api/countries` | List all countries (supports filters & sorting) |
| `GET` | `/api/countries/<name>` | Retrieve a country by name |
| `DELETE` | `/api/countries/<name>` | Delete a country |
| `GET` | `/api/countries/status` | Returns total countries & last refresh timestamp |
| `GET` | `/api/countries/image` | Returns summary image (top 5 countries by GDP) |
| `GET` | `/api/docs/` | Swagger documentation |

---

## 🧭 Query Parameters

| Parameter | Description | Example |
|------------|--------------|----------|
| `region` | Filter by region | `/api/countries?region=Africa` |
| `currency` | Filter by currency code | `/api/countries?currency=NGN` |
| `sort` | Sort by GDP | `/api/countries?sort=gdp_desc` or `/api/countries?sort=gdp_asc` |

---

## 🧾 Example Responses

### ✅ Successful Refresh
```json
{
  "message": "Refresh successful",
  "total_countries": 250,
  "last_refreshed_at": "2025-10-22T18:00:00Z"
}
```

### ✅ Country List
```json
[
  {
    "id": 1,
    "name": "Nigeria",
    "capital": "Abuja",
    "region": "Africa",
    "population": 206139589,
    "currency_code": "NGN",
    "exchange_rate": 1600.23,
    "estimated_gdp": 25767448125.2,
    "flag_url": "https://flagcdn.com/ng.svg",
    "last_refreshed_at": "2025-10-22T18:00:00Z"
  }
]
```

### ⚠️ Validation Error
```json
{
  "error": "Validation failed",
  "details": {
    "currency_code": "is required"
  }
}
```

### ⚠️ Not Found
```json
{
  "error": "Country not found"
}
```

### ⚠️ External API Failure
```json
{
  "error": "External data source unavailable",
  "details": "Could not fetch data from Exchange Rates API"
}
```

---

## 🖼️ Summary Image Example

Generated at `cache/summary.png` after a successful refresh.

Accessible at:
```
GET /api/countries/image
```

If image not found:
```json
{ "error": "Summary image not found" }
```

---

## 📚 Documentation

OpenAPI / Swagger UI is available at:
```
http://127.0.0.1:8000/api/docs/
```

Schema JSON at:
```
http://127.0.0.1:8000/api/schema/
```

---

## ⚠️ Error Handling Summary

| HTTP Code | Description | Example |
|------------|--------------|----------|
| `400` | Validation failed | `{ "error": "Validation failed", "details": {...} }` |
| `404` | Not found | `{ "error": "Country not found" }` |
| `503` | External API error | `{ "error": "External data source unavailable", "details": "..." }` |
| `500` | Server error | `{ "error": "Internal server error" }` |

---

## 🧠 Notes

- The refresh endpoint uses **transactions** to prevent partial updates.  
- Each refresh call recalculates a new random multiplier (1000–2000) for every country.  
- Countries with no currency or missing exchange rate are still stored, per spec.  
- The last refresh timestamp is updated for all countries on each refresh.  
- If external APIs fail, no database changes are made.  

---

## 🧰 Developer Notes

**Environment Variables (.env):**
```
DB_NAME=hngstage2
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=3306
SECRET_KEY=your_project_secret_key
DEBUG=True_or_False(your choice)
```

**Dependencies (summary):**
```
Django
djangorestframework
drf-spectacular
mysqlclient
requests
Pillow
python-dotenv
```

---

## 🧪 Testing

Run migrations and test endpoints using `curl` or Postman.

Example tests:

```bash
# Trigger refresh
curl -X POST http://127.0.0.1:8000/countries/refresh

# Get all countries
curl http://127.0.0.1:8000/countries

# Filter by region
curl http://127.0.0.1:8000/countries?region=Africa

# Get summary image
curl -O http://127.0.0.1:8000/countries/image
```

---

## ☁️ Deployment

You can deploy on:
- **Railway**
- **Heroku**
- **AWS**
- **PXXL App**




## 👤 Author

**Name:** *Rita-Mary Amakom*  
**Project:** HNG Stage 2 Backend — Country Currency & Exchange API  
**GitHub:** [Rita-Mary](https://github.com/Rita-Mary)  
**Email:** *(amakomritamary322@gmail.com)*  

---

## 🏁 License

This project is open-source and free to use for educational purposes.

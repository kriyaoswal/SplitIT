# Split App Backend API

A backend service built with **FastAPI** and **MongoDB Atlas** that enables users to log shared expenses, compute individual balances, and suggest minimal settlements. This project is part of a backend engineering assessment.

---

## Features Implemented

✅ Add, update, delete shared expenses  
✅ Track who paid and who owes whom  
✅ Auto-calculate balances  
✅ Suggest minimal settlements  
✅ Fetch unique list of people  
✅ MongoDB Atlas integration (asynchronous with `motor`)  
✅ Swagger UI & ReDoc API documentation  
✅ Timestamps (`created_at`) on every expense  
✅ Custom error responses (JSON structured)  
✅ Postman collection included for testing

---

## Folder Structure

```
SplitApp/
├── main.py                  # FastAPI backend
├── .env                     # MongoDB URI (not included)
├── SplitApp.postman_collection.json
└── requirements.txt         # Dependencies
```

---

##  Tech Stack

- **FastAPI** for API layer  
- **MongoDB Atlas** with `motor` async driver  
- **Pydantic** for schema validation  
- **Uvicorn** as ASGI server  
- **dotenv** for environment variable management

---

## 📬 API Endpoints

| Method | Endpoint              | Description                      |
|--------|-----------------------|----------------------------------|
| POST   | `/expenses`           | Add a new expense                |
| GET    | `/expenses`           | Retrieve all expenses            |
| PUT    | `/expenses/{id}`      | Update an existing expense       |
| DELETE | `/expenses/{id}`      | Delete an expense by ID          |
| GET    | `/people`             | Get all unique users             |
| GET    | `/balances`           | View how much each user owes     |
| GET    | `/settlements`        | Suggested payments to settle all |

---

## 🧪 Testing via Postman

A fully functional Postman collection is included:

- ✅ `SplitApp.postman_collection.json`
- Covers all endpoints with sample payloads
- Easy to test locally at `http://localhost:8000`

---

## 🌐 API Docs

- Swagger UI → `http://localhost:8000/docs`
- ReDoc UI → `http://localhost:8000/redoc`

---

## 🗃 Sample Payloads

### ✅Add Expense
```json
{
  "amount": 900,
  "description": "Dinner",
  "paid_by": "Shantanu",
  "shared_with": ["Sanket", "Om"]
}
```

### ✅ Add Expense with Custom Shares
```json
{
  "amount": 900,
  "description": "Dinner",
  "paid_by": "Shantanu",
  "shared_with": ["Sanket", "Om"],
  "shares": {
    "Sanket": 300,
    "Om": 200
  }
}
```

---

## ✅ Extras Implemented

- [x] `created_at` timestamp in every expense
- [x] Structured custom error messages
- [x] MongoDB `_id` stripped for clean responses
- [x] Compatible with Swagger + Postman
- [x] Tested against expected use cases

---

## Note on Swagger UI

The Swagger UI might briefly show a validation placeholder error block — this is **just Swagger's example schema**, not an actual API error. It disappears once valid payloads are submitted.

---

## Notes

- No authentication layer added (not required by assignment)
- Deployment optional — app runs on `localhost:8000`

---

## 👤 Author

Kriya Oswal  
GitHub: https://github.com/kriyaoswal 
FastAPI Project for Backend Internship Assignment

# main.py (Split App API)
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from uuid import uuid4
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

app = FastAPI(title="SplitIT")

# MongoDB Atlas connection
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.splitapp
expenses = db.expenses

# Error handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

# Models
class ExpenseCreate(BaseModel):
    amount: float
    description: str
    paid_by: str
    shared_with: List[str]
    shares: Optional[Dict[str, float]] = None

class Expense(ExpenseCreate):
    id: str
    created_at: str

# API Endpoints
@app.post("/expenses", response_model=Expense)
async def add_expense(expense: ExpenseCreate):
    new_expense = expense.dict()
    new_expense["id"] = str(uuid4())
    new_expense["created_at"] = datetime.utcnow().isoformat()
    await expenses.insert_one(new_expense)
    return new_expense

@app.get("/expenses", response_model=List[Expense])
async def get_expenses():
    docs = await expenses.find().to_list(100)
    for doc in docs:
        doc.pop("_id", None)
        if "created_at" not in doc:
            doc["created_at"] = "N/A"
    return docs


@app.put("/expenses/{expense_id}", response_model=Expense)
async def update_expense(expense_id: str, updated: ExpenseCreate):
    updated_data = updated.dict()
    updated_data["created_at"] = datetime.utcnow().isoformat()
    result = await expenses.find_one_and_update(
        {"id": expense_id}, {"$set": updated_data}, return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Expense not found")
    result["id"] = expense_id
    return result

@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: str):
    result = await expenses.delete_one({"id": expense_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}

@app.get("/people")
async def get_people():
    people = set()
    entries = await expenses.find().to_list(100)
    for e in entries:
        people.add(e["paid_by"])
        people.update(e["shared_with"])
    return list(people)

@app.get("/balances")
async def get_balances():
    balances = {}
    entries = await expenses.find().to_list(100)
    for e in entries:
        amount = e["amount"]
        if e.get("shares"):
            for person, share in e["shares"].items():
                balances[person] = balances.get(person, 0) - share
            balances[e["paid_by"]] = balances.get(e["paid_by"], 0) + amount
        else:
            split = round(amount / len(e["shared_with"]), 2)
            for person in e["shared_with"]:
                balances[person] = balances.get(person, 0) - split
            balances[e["paid_by"]] = balances.get(e["paid_by"], 0) + amount
    return balances

@app.get("/settlements")
async def get_settlements():
    balances = await get_balances()
    creditors = [(p, amt) for p, amt in balances.items() if amt > 0]
    debtors = [(p, -amt) for p, amt in balances.items() if amt < 0]

    settlements = []
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        d_person, d_amt = debtors[i]
        c_person, c_amt = creditors[j]
        settle_amt = min(d_amt, c_amt)
        settlements.append({"from": d_person, "to": c_person, "amount": round(settle_amt, 2)})
        debtors[i] = (d_person, d_amt - settle_amt)
        creditors[j] = (c_person, c_amt - settle_amt)
        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1
    return settlements

import sys
import os
from typing import List, Dict, Any
from fastapi import APIRouter, Query

# --- NEW PATH FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --- END OF NEW PATH FIX ---

from src.utils.fraud_dashboard.database import get_collection

router = APIRouter(prefix="/transactions", tags=["Transactions"])

try:
    collection = get_collection("transactions")
except Exception as e:
    print(f"CRITICAL ERROR in transactions.py: Could not get 'transactions' collection. {e}")
    collection = None


@router.get("/")
def list_transactions(limit: int = Query(100, ge=1, le=2000), offset: int = Query(0, ge=0)) -> List[Dict[str, Any]]:
    """Return a paginated list of transactions (no PII)"""
    if collection is None:
        return {"error": "Database connection failed"}

    cursor = (
        collection.find({}, {"_id": 0}).sort("timestamp", -1).skip(offset).limit(limit)
    )
    return list(cursor)


@router.get("/{transaction_id}")
def get_transaction(transaction_id: str):
    if collection is None:
        return {"error": "Database connection failed"}
    doc = collection.find_one({"transaction_id": transaction_id}, {"_id": 0})
    if not doc:
        return {"error": "not_found"}
    return doc

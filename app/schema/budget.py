from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.budget import CategoryEnum


# When Sarpanch adds govt allocated budget

class BudgetCreate(BaseModel):
    financial_year : str                # Required -- "2024-25"
    total_allocated : float             # Required (50 Lakhs)
    description : Optional[str] = None  # optional — "14th Finance Commission funds"
    

# For update budget detail

class BudgetUpdate(BaseModel):
    total_allocated: Optional[float] = None
    description: Optional[str] = None
    
# What we send back after creating budget 

class BudgetResponse(BaseModel):
    id: int                  # auto — 1, 2, 3...
    village_id: int          # which village
    financial_year: str      # "2024-25"
    total_allocated: float   # 5000000.00 (₹50 lakh)
    total_spent: float       # 0.0 initially, increases with transactions
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
        
 
# When Head/Sarpanch want to record transaction of a budget 


class TransactionCreate(BaseModel):
    budget_id: int          # required — which budget (1, 2...)
    category: CategoryEnum  # required — "road" / "water" / "health" etc.
    amount: float           # required — 150000.00 (₹1.5 lakh)
    description: str        # required — "Road repair material purchased"
    
# What we send back after create transaction 

class TransactionResponse(BaseModel):
    id: int                  # auto — 1, 2, 3...
    budget_id: int           # which budget
    category: CategoryEnum   # "road"
    amount: float            # 150000.00
    description: str         # "Road repair material purchased"
    date: datetime           # when transaction was added

    class Config:
        from_attributes = True                
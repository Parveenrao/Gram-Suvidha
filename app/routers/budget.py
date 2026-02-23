from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.budget import Budget, BudgetTransaction, CategoryEnum
from app.models.user import RoleEnum
from app.schema.budget import BudgetCreate, BudgetResponse, TransactionCreate, TransactionResponse , BudgetUpdate
from app.utils.auth import get_current_user
from app.utils.exception import ConflictException  , NotFoundException , UnauthorizeException , ForbiddenException ,  BadRequestException

router = APIRouter()


#------------------------------------------ Public Enpoints-----------------------------------------------



# Get all budget

@router.get("/" , response_model=List[BudgetResponse])

def get_all_budgets(village_id : int , db :Session = Depends(get_db)):
    
    """
    Get all budgets of a village.
    Public — any citizen can view.
    Example: /api/budget/?village_id=1
    """
    
    budget = db.query(Budget).filter(Budget.village_id == village_id).order_by(Budget.created_at.desc()).all()
    
    return budget

# Get budget by id 

@router.get("/{budget_id}" , response_model=List[BudgetResponse])

def get_budget_by_id(budget_id :int  , db:Session = Depends(get_db)):
    
    """
    Get single budget by ID.
    Public — anyone can view.
    """
    
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    
    if not budget:
        raise NotFoundException("Budget not found")
    
    return budget

# Get transaction / spending  of budget 

@router.get("/{budget_id}/transaction", response_model=List[BudgetResponse])

def get_transaction(budget_id : int  , db : Session = Depends(get_db)):
    
    """
    Get all transactions/spendings of a budget.
    Public — citizens can see where money was spent.
    This is the core transparency feature! 💰
    """
    
    # check budget exist 
    
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    
    if not budget:
        raise NotFoundException("Budget not found")
    
    # get transcation 
    
    transactions  = db.query(BudgetTransaction).filter(BudgetTransaction.budget_id == budget_id).order_by(BudgetTransaction.date.desc()).all()
    
    return transactions

# Get transaction filter by category 

@router.get("/{budget_id}/transaction/category{category}" , response_model=List[BudgetResponse])

def get_transaction_category(budget_id :int , category : CategoryEnum, db : Session = Depends(get_db)):
    
    """
    Get transactions filtered by category.
    Example: /api/budget/1/transactions/category/road
    Types: road / water / sanitation / education / health / electricity / agriculture / other
    """
    # check budget exist 
    
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    
    if not budget:
        raise NotFoundException("Budget not found")
    
    
    # get transaction by category 
    
    transaction = db.query(BudgetTransaction).filter(BudgetTransaction.budget_id == budget_id , BudgetTransaction.category == category).order_by(
        BudgetTransaction.date.desc()).all()
    
    return transaction

# Get full bueget summary 


@router.get("/{budget_id}/summary")

def get_budget_summary(budget_id : int , db : Session = Depends(get_db)):
    
    """
    Get full budget summary with category wise breakdown.
    Public — citizens can see full spending breakdown.
    Perfect for transparency dashboard! 
    """
    
    #check budget exist 
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    
    if not budget:
        raise NotFoundException("Budget not found")
    
    # categroy wise breakdown 
    
    rows = (db.query(BudgetTransaction.category , func.sum(BudgetTransaction.category)).filter(
                           BudgetTransaction.budget_id == budget_id).group_by(BudgetTransaction.category).all())   #will return category enum
    
    # intialize all category with 0 
    
    category_breakdown = {c.value : 0 for c in CategoryEnum}
    
    # Fill actual totals 
    
    for category , total in rows:
        category_breakdown[category.value] = float(total , 0)
        
    remaining = budget.total_allocated - budget.total_spent
    
    spent_percentage =  ( (budget.total_spent / budget.total_allocated) * 100)
    
    return {
        "financial_year": budget.financial_year,
        "total_allocated": budget.total_allocated,
        "total_spent": budget.total_spent,
        "remaining": remaining,
        "spent_percentage": round(spent_percentage, 2),
        "category_breakdown": category_breakdown
    }
    
    
#----------------------- Sarpanch / Admin enpoints-----------------------------------

# create budget 

@router.post("/" , response_model=BudgetResponse , status_code=201)

def create_budget(data : BudgetCreate , db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    SARPANCH / ADMIN ONLY — Create new budget for a financial year.
    Only one budget per financial year per village allowed.
    """
    
    # check role 
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin]:
        raise ForbiddenException("Access Denied")
    
    
    # check budget already exist for this financial year 
    
    budget = db.query(Budget).filter(Budget.village_id == current_user.village_id , Budget.financial_year == data.financial_year).first()
    
    if budget:
        raise ConflictException("Budget already exist for the financial year")
    
    budget = Budget(financial_year = data.financial_year ,
                    total_allocated = data.total_allocated,
                    description = data.description,
                    village_id = current_user.village_id,
                    total_spend = 0.0)
    
    db.add(budget)
    db.commit()
    db.refresh(budget)
    
    
# Partial update the budget details 

@router.patch("/{budget_id}" , response_model=BudgetResponse) 

def update_budget(budget_id : int , data : BudgetUpdate ,  db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    # check role 
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin]:
        raise ForbiddenException("Access Denied")
    
    # get budget 
    
    budget = db.query(Budget).filter(Budget.id == budget_id , Budget.village_id == current_user.village_id).first()
    
    if not budget:
        raise NotFoundException("Budget not found")
    
    
    update_data = data.model_dump(exclude_unset=True)
    
    for key , value in update_data.items():
        setattr(Budget , key , value)
        
    db.commit()
    db.refresh(budget)
    
    return budget


# Delete budget by id 

@router.delete("/{budget_id}")

def delete_budget(budget_id , db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    ADMIN ONLY — Delete a budget and all its transactions.
    """
    
    # check role 
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin]:
        raise ForbiddenException("Access Denieed")
    
    # check budget 
    
    budget = db.query(Budget).filter(Budget.id , budget_id , Budget.vilage_id == current_user.village_id).first()
    
    if not budget:
        raise NotFoundException("Budget not found")
    
    # delete transcation of budget 
    
    db.query(BudgetTransaction).filter(BudgetTransaction.budget_id == budget_id).delete()
    
    
    db.delete(budget)
    
    db.commit()
    
    return {"message": f"Budget for {budget.financial_year} deleted successfully"}    


# -------- Transaction Endpoints--------------------------------


# Create Transactions 

@router.post("/transaction" , response_model=TransactionResponse , status_code=201)

def create_budget_transaction(data : TransactionCreate , db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    
    """
    SARPANCH / ADMIN ONLY — Record a new spending/transaction.
    Automatically updates total_spent in budget.
    """
    
    # role check 
    
    if current_user.role not in [RoleEnum.admin , RoleEnum.sarpanch]:
        raise ForbiddenException("Access Denied")
    
    # check budget exist and belong to same village 
    
    budget = db.query(Budget).filter(Budget.id == data.budget_id , Budget.village_id == current_user.village_id).first()
    
    if not budget:
        raise NotFoundException("Budget not found")
    
    # check spending doest not exceed allocated amount 
    
    remaining = budget.total_allocated - budget.total_spent
    
    if data.amount > remaining:
        raise BadRequestException("Amount does not exceed remaining amount")
    
    # create transaction 
    
    transaction = BudgetTransaction(budget_id = data.budget_id,
                                    category = data.category,
                                    amount = data.amount,
                                    description = data.description,
                                    spent_by = current_user.id
                                    )
    
    db.add(transaction)
    
    # add total spent in budget table 
    
    budget.total_spent += data.amount
    
    db.commit()
    db.refresh(transaction)
    
    return transaction


# delete transaction 

@router.delete("/transaction/{transaction_id}")

def delete_transaction(transaction_id : int ,  db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    ADMIN ONLY — Delete a transaction.
    Also reduces total_spent in budget automatically.
    """
    
    # role check
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin]:
        raise ForbiddenException("Access Denied")
    
    # delete transaction 
    
    transaction = db.query(BudgetTransaction).filter(BudgetTransaction.id == transaction_id).first()
    
    if not transaction:
        raise NotFoundException("Transaction not found")
    
    # Reduce total spent 
    
    budget = db.query(Budget).filter(Budget.id == transaction.budget_id).first()
    
    if budget:
        budget.total_allocated -= transaction.amount
    
    db.delete(transaction)
    db.commit()
    
    return {"message": "Transaction deleted successfully"}    

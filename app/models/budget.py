from sqlalchemy import Column , String , DateTime , ForeignKey , Enum , Float , Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class CategoryEnum(str ,enum.Enum):
    road = "road"
    water = "water"
    sanitation = "sanitation"
    education = "education"
    health = "health"
    electricity = "electricity"
    agriculture = "agriculture"
    other = "other"
    
    
class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer , primary_key=True , index=True)
    village_id = Column(Integer , ForeignKey("villages.id") , nullable=False)
    financial_year = Column(String , nullable=False)   #eg. "2024-25"
    total_allocated = Column(Float , nullable=False)   # Govt Allocated budget
    total_spent = Column(Float , default=0.0) 
    description = Column(String , nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
    # Relationship 
    
    village = relationship("Village", back_populates="budgets")
    transactions = relationship("BudgetTransaction", back_populates="budget")
    
    
    
    
class BudgetTransaction(Base):
    __tablename__ = "budget-transactions"
    
    id = Column(Integer , primary_key=True , index=True)
    budget_id = Column(Integer , ForeignKey("budgets.id")  , nullable=False) 
    category = Column(Enum(CategoryEnum) , nullable=False)
    amount  = Column(Float , nullable=False)
    description = Column(String , nullable=False)
    spent_by = Column(Integer , ForeignKey("users.id"))   # sarpanch who added
    date = Column(DateTime(timezone=True) , server_default=func.now())
    
    # Relationship 
    
    budget = relationship("Budget", back_populates="transactions")
    
           
    
    
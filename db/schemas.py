from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, condecimal


# USER SCHEMAS
class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


# INSTRUMENT SCHEMAS
class InstrumentBase(BaseModel):
    symbol: str
    name: Optional[str] = None
    category: Optional[str] = None


class InstrumentCreate(InstrumentBase):
    pass


class InstrumentResponse(InstrumentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# TRANSACTION SCHEMAS
class TransactionCreate(BaseModel):
    instrument_id: int
    type: str  # "BUY" or "SELL"
    units: float
    price: float


class TransactionResponse(BaseModel):
    user_id: int
    symbol: str
    type: str
    units: float
    price: float
    date: date

    class Config:
        from_attributes = True



# HOLDING SCHEMAS
class HoldingBase(BaseModel):
    instrument_id: int
    total_units: float
    average_cost: float
    
    
from pydantic import BaseModel
from typing import List


class HoldingSummary(BaseModel):
    symbol: str
    name: str
    total_units: float
    average_cost: float
    current_price: float
    total_invested: float
    current_value: float
    profit_loss: float



class HoldingResponse(HoldingBase):
    id: int
    user_id: int
    last_updated: datetime
    instrument: Optional[InstrumentResponse] = None

    class Config:
        from_attributes = True


# PORTFOLIO SUMMARY SCHEMA (for custom endpoint)
class PortfolioSummary(BaseModel):
    total_value: float
    total_cost: float
    total_returns: float
    holdings: List[HoldingSummary]



# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Date,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship
from db.database import Base
import enum

class TransactionType(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

# User Table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    holdings = relationship("Holding", back_populates="user", cascade="all, delete-orphan")
    

# INSTRUMENTS TABLE
class Instrument(Base):
    __tablename__ = "instruments"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, nullable=False)
    name = Column(String(100))
    category = Column(String(50))  # e.g. Stock, Mutual Fund
    created_at = Column(TIMESTAMP, default=datetime.now)

    # Relationships
    transactions = relationship("Transaction", back_populates="instrument", cascade="all, delete-orphan")
    holdings = relationship("Holding", back_populates="instrument", cascade="all, delete-orphan")


# TRANSACTIONS TABLE
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    instrument_id = Column(Integer, ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(10), CheckConstraint("type IN ('BUY', 'SELL')"), nullable=False)
    units = Column(Numeric(12, 4), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    transaction_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="transactions")
    instrument = relationship("Instrument", back_populates="transactions")


# HOLDINGS TABLE
class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    instrument_id = Column(Integer, ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False)
    total_units = Column(Numeric(12, 4), default=0)
    average_cost = Column(Numeric(12, 2), default=0)
    last_updated = Column(TIMESTAMP, default=datetime.now)

    # Relationships
    user = relationship("User", back_populates="holdings")
    instrument = relationship("Instrument", back_populates="holdings")

    __table_args__ = (UniqueConstraint("user_id", "instrument_id", name="unique_user_instrument"),)
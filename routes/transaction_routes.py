from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User, Instrument, Transaction, Holding
from db.schemas import TransactionCreate, TransactionResponse
from core.security import get_current_user
from datetime import date
from sqlalchemy import func, case

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_user_holdings(db: Session, user_id: int, instrument_id: int) -> float:
    """Calculate total units currently held by a user for a given instrument."""
    return (
        db.query(
            func.sum(
                case(
                    (Transaction.type == "BUY", Transaction.units),
                    (Transaction.type == "SELL", -Transaction.units),
                    else_=0,
                )
            )
        )
        .filter(Transaction.user_id == user_id, Transaction.instrument_id == instrument_id)
        .scalar()
        or 0
    )


@router.post("/", response_model=TransactionResponse)
def add_transaction_by_current_user(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Adds a transaction (BUY/SELL) and updates holdings for the current logged-in user."""

    # Validate instrument
    instrument = db.query(Instrument).filter(Instrument.id == transaction.instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")

    # Get current holding (if any)
    holding = (
        db.query(Holding)
        .filter(Holding.user_id == current_user.id, Holding.instrument_id == instrument.id)
        .first()
    )

    current_units = holding.total_units if holding else 0

    # Prevent overselling
    if transaction.type == "SELL" and transaction.units > current_units:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot sell {transaction.units} units — only {current_units} units available.",
        )

    # Record transaction
    new_txn = Transaction(
        user_id=current_user.id,
        instrument_id=instrument.id,
        type=transaction.type,
        units=transaction.units,
        price=transaction.price,
        transaction_date=date.today(),
    )
    db.add(new_txn)

    # Update or create holding
    if transaction.type == "BUY":
        if holding:
            # Recalculate average cost
            total_cost = float(holding.average_cost) * float(holding.total_units)
            new_cost = total_cost + (float(transaction.price) * float(transaction.units))
            new_units = float(holding.total_units) + float(transaction.units)
            holding.total_units = new_units
            holding.average_cost = new_cost / new_units
            holding.last_updated = date.today()
        else:
            holding = Holding(
                user_id=current_user.id,
                instrument_id=instrument.id,
                total_units=transaction.units,
                average_cost=transaction.price,
                last_updated=date.today(),
            )
            db.add(holding)

    elif transaction.type == "SELL":
        if holding:
            remaining_units = float(holding.total_units) - float(transaction.units)
            if remaining_units <= 0:
                # Remove holding if fully sold
                db.delete(holding)
            else:
                holding.total_units = remaining_units
                holding.last_updated = date.today()

    # Commit all changes
    db.commit()
    db.refresh(new_txn)

    # Response
    response_txn = TransactionResponse(
        user_id=new_txn.user_id,
        symbol=instrument.symbol,
        type=new_txn.type,
        units=float(new_txn.units),
        price=float(new_txn.price),
        date=new_txn.transaction_date,
    )

    return response_txn


@router.get("/", response_model=list[TransactionResponse])
def get_all_my_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Gets transaction history for the current logged-in user."""
    transactions = (
        db.query(Transaction)
        .join(Instrument)
        .filter(Transaction.user_id == current_user.id)
        .all()
    )
    return [
        TransactionResponse(
            user_id=txn.user_id,
            symbol=txn.instrument.symbol,
            type=txn.type,
            units=float(txn.units),
            price=float(txn.price),
            date=txn.transaction_date,
        )
        for txn in transactions
    ]


@router.get("/{user_id}", response_model=list[TransactionResponse])
def get_transactions_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """Gets transaction history for a specific user by user_id."""
    transactions = (
        db.query(Transaction)
        .join(Instrument)
        .filter(Transaction.user_id == user_id)
        .all()
    )
    return [
        TransactionResponse(
            user_id=txn.user_id,
            symbol=txn.instrument.symbol,
            type=txn.type,
            units=float(txn.units),
            price=float(txn.price),
            date=txn.transaction_date,
        )
        for txn in transactions
    ]

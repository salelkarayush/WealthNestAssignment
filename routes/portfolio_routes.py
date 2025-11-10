from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User, Holding
from db.schemas import PortfolioSummary, HoldingSummary
from core.security import get_current_user
import json
from core.price_utils import load_prices as load_local_prices

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/", response_model=PortfolioSummary)
def get_portfolio_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get portfolio summary for current user, including weighted average cost and profit/loss per instrument."""
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()
    prices_data = load_local_prices()

    total_value = total_cost = total_returns = 0.0
    holding_summaries = []

    for holding in holdings:
        symbol = holding.instrument.symbol
        name = holding.instrument.name

        total_units = float(holding.total_units or 0)
        avg_cost = float(holding.average_cost or 0)
        latest_price = prices_data.get(symbol)

        if latest_price is None or total_units == 0:
            continue

        latest_price = float(latest_price)

        current_value = total_units * latest_price
        total_invested = total_units * avg_cost
        profit_loss = current_value - total_invested

        total_cost += total_invested
        total_value += current_value
        total_returns += profit_loss

        holding_summaries.append(
            HoldingSummary(
                symbol=symbol,
                name=name,
                total_units=round(total_units, 4),
                average_cost=round(avg_cost, 2),
                current_price=round(latest_price, 2),
                total_invested=round(total_invested, 2),
                current_value=round(current_value, 2),
                profit_loss=round(profit_loss, 2),
            )
        )

    return PortfolioSummary(
        total_value=round(total_value, 2),
        total_cost=round(total_cost, 2),
        total_returns=round(total_returns, 2),
        holdings=holding_summaries,
    )

from fastapi import APIRouter
from routes import (user_routes,
                    login_routes, 
                    instrument_routes,
                    transaction_routes, 
                    portfolio_routes)

base_router = APIRouter()

base_router.include_router(user_routes.router)
base_router.include_router(login_routes.router)
base_router.include_router(instrument_routes.router)
base_router.include_router(transaction_routes.router)
base_router.include_router(portfolio_routes.router)

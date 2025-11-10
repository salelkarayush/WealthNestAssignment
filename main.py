from fastapi import FastAPI
from db.database import  engine, Base
from core.config import settings
from routes.base import base_router
import uvicorn
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME
)

#routes main to all other routes
app.include_router(base_router)


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}!"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
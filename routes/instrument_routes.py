from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import schemas, models, database

router = APIRouter(prefix="/instruments", tags=["Instruments"])

@router.post("/", response_model=schemas.InstrumentResponse)
def create_instrument(instrument: schemas.InstrumentCreate, db: Session = Depends(database.get_db)):
    """Creates a new instrument in the database. """
    db_instrument = db.query(models.Instrument).filter(models.Instrument.symbol == instrument.symbol).first()
    if db_instrument:
        raise HTTPException(status_code=400, detail="Instrument already exists")
    new_instrument = models.Instrument(**instrument.model_dump())
    db.add(new_instrument)
    db.commit()
    db.refresh(new_instrument)
    return new_instrument


@router.get("/", response_model=list[schemas.InstrumentResponse])
def get_all_instruments(db: Session = Depends(database.get_db)):
    """ Get all Instruments """
    return db.query(models.Instrument).all()

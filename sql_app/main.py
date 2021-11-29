from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import get_db, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI(title="Sadajiwa Checkout")


@app.post("/orders/", response_model = str, tags=["order"])
def order(pesanan : schemas.PesananCreate,db: Session = Depends(get_db)):
    db_order = crud.create_order(db,pesanan)
    db_orderitems = crud.create_item_order(db, pesanan, db_order.id_pesanan)
    return "order_done"
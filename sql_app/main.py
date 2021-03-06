from typing import Dict, List

from sqlalchemy.util.langhelpers import NoneType
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

@app.get("/orders/{id_order}", response_model=schemas.Pesanan, tags=["getters"])
def get_order(id_order: int, db: Session = Depends(get_db)):
    return crud.get_order(db,id_order)

@app.get("/products/{id_product}")
def get_product(id_product:int, db: Session = Depends(get_db), tags=["getters"]):
    return crud.get_product(db,id_product)

@app.get("/order_items/{id_order}", response_model = List[schemas.ItemPesanan], tags=["getters"])
def get_order_items(id_order: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_order_items(db,id_order)
# def get_order_items()

@app.get("/benefits/{id_benefit}", response_model=schemas.Benefit, tags=["getters"])
def get_benefit(id_benefit: int, db: Session = Depends(get_db)):
    return crud.get_benefit(db,id_benefit)

@app.post("/orders/", response_model = schemas.Pesanan, tags=["order"])
def order(pesanan : schemas.PesananCreate,db: Session = Depends(get_db)):
    
    check_kuantitas = False
    for item in pesanan.produk:
        if item.kuantitas >0:
            check_kuantitas = True
    if not check_kuantitas:
        raise HTTPException(status_code=403, detail="No items ordered")

    db_order = crud.create_order(db,pesanan)

    if db_order is None:
        raise HTTPException(status_code=404, detail= "Order details invalid")

    db_orderitems = []
    for item in pesanan.produk:
        item_ordered = crud.create_item_order(db, item, db_order.id_pesanan)
        if pesanan.total_harga == 0:
            crud.add_order_harga(db,db_order.id_pesanan,item_ordered.total_harga_produk)
        db_orderitems.append(item_ordered)
    if (hasattr(pesanan,"id_benefit") and (pesanan.id_benefit != None)):
        db_order = crud.apply_benefit(db,db_order.id_pesanan,pesanan.id_benefit) #Update Schemanya
    return db_order

@app.patch("/orders/", response_model = schemas.Pesanan, tags=["order"])
def update_order(update : schemas.PesananUpdate, db: Session = Depends(get_db)):
    orders = crud.update_order(db,update)# tambahin exception kalau salah
    return orders

@app.patch("/orders/{harga}", response_model = schemas.Pesanan, tags=["order"])
def update_order(id_pesanan: int, update_harga : int, db: Session = Depends(get_db)):
    db_order = crud.add_order_harga(db,id_pesanan, update_harga)
    return db_order

# @app.patch("/orders/status", response_model = dict, tags=["order"])
# def update_order(update : schemas.PesananUpdate, db: Session = Depends(get_db)):
#     orders = crud.update_order(db,update)# tambahin exception kalau salah
#     return orders
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Sadajiwa Checkout",
              description="18219047", openapi_tags="checkout_products")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Post Menu (Add New Menu Item)
# @app.post("/orders/")
# async def order(pesanan : schemas.PesananCreate, item: schemas.ItemPesananCreate,db: Session = Depends(get_db)):
#     db_order = crud.create_order(db,pesanan)
#     db_orderitems = crud.create_item_order(db, item, db_order.id_pesanan)
#     return db_order,db_orderitems

# @app.patch("/orders/")
# async def update_item(status : schemas.Status):
#     status_dict = status.dict()
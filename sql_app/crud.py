from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.sql.expression import delete

from sql_app import database
from . import models, schemas
from datetime import datetime, timedelta
from typing import Optional


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.product_id == product_id).first()

def get_benefit(db: Session, benefit_id: int):
    return db.query(models.Benefit).filter(models.Benefit.id_benefit == benefit_id).first()

def get_item_order(db: Session, id_item: int, id_order: int):
    return db.query(models.item_pesanan).filter((models.item_pesanan.id_pesanan == id_order) and 
    (models.item_pesanan.id_produk == id_item))

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id_pesanan == order_id).first()

def get_order_items(db: Session, order_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.item_pesanan).filter(models.item_pesanan.id_pesanan == order_id).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.PesananCreate):
    db_order = models.Order(id_user = order.id_user, nama_pemesan = order.nama_pemesan, no_telepon = order.no_telepon, 
                        alamat_pengiriman = order.alamat_pengiriman, metode_pembayaran = order.metode_pembayaran, ekspedisi = order.ekspedisi,
                        total_harga = order.total_harga, status_pesanan = order.status_pesanan)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def create_item_order(db: Session, item: schemas.PayloadPesanan, pesanan: int):
    harga_produk = item.kuantitas * (get_product(db,item.id_produk).harga)
    db_item = models.item_pesanan(id_pesanan = pesanan, id_produk = item.id_produk, kuantitas= item.kuantitas, 
    total_harga_produk = harga_produk, notes = item.notes) #update total harga
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    update_item_stock(db,item.id_produk, -1)
    #add_order_harga(db,pesanan,harga_produk)
    return db_item

def update_item_stock(db: Session, item: int, qty: int):
    db_product_stock = get_product(db,item) + qty
    if(db_product_stock <= 0):
        db_product_stock = 0
    db.query(models.Product.id_pesanan == item).update({"stok" : db_product_stock})

def update_order_status(db:Session, id_order: int, status_change: str):
    db_order = get_order(db, id_order)
    db.query(models.Order).filter(models.Order.id_pesanan == id_order).update({"status_pesanan":status_change}, synchronize_session = "fetch")
    db.commit()
    db.refresh(db_order)


def add_order_harga(db:Session, id_order: int, update_harga: int):
    db_order = get_order(db, id_order)
    harga_total = db_order.total_harga + update_harga
    db.query(models.Order).filter(models.Order.id_pesanan == id_order).update({"total_harga": harga_total}, synchronize_session = "fetch")
    db.commit()
    db.refresh(db_order)

def update_order(db: Session, order: schemas.PesananUpdate):
    db_order = get_order(db, order.id_pesanan)
    db.query(models.Order).filter(models.Order.id_pesanan == order.id_pesanan).update(dict(order))
    db.commit()
    db.refresh(db_order)
    return db_order

def apply_benefit(db: Session, id_order: int, id_benefit: int):
    db_order = get_order(db, id_order)
    db_benefit_diskon = get_benefit(db,id_benefit)
    harga_update = db_order.total_harga - db_benefit_diskon.diskon
    db_order.update({"total_harga": harga_update}, synchronize_session = "fetch")


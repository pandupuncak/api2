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

def create_order(db: Session, order: schemas.PesananCreate):
    db_order = models.Order(id_user = order.id_user, nama_pemesan = order.nama_pemesan, no_telepon = order.no_telepon, 
                        alamat_pengiriman = order.alamat_pengiriman, metode_pembayaran = order.metode_pembayaran, ekspedisi = order.ekspedisi,
                        total_harga = order.total_harga, status_pesanan = order.status_pesanan)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def create_item_order(db: Session, item: schemas.PesananCreate, pesanan: int):
    harga_produk = item.kuantitas * (get_product(db,item.id_produk).harga)
    db_item = models.item_pesanan(id_pesanan = pesanan, id_produk = item.id_produk, kuantitas= item.kuantitas, 
    total_harga_produk = harga_produk, notes = item.notes) #update total harga
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
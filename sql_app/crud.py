from sqlalchemy.orm import Session



from . import models, schemas




def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(models.User.id == user_id).first()




def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.product_id == product_id).first()

def get_benefit(db: Session, benefit_id: int):
    return db.query(models.Benefit).filter(models.Benefit.id_benefit == benefit_id).first()

def create_order(db: Session, order: schemas.PesananCreate):
    db_order = models.Order(id_user = order.id_user, nama_pemesan = order.nama_pemesan, no_telepon = order.no_telepon, 
    alamat_pengiriman = order.alamat_pengiriman, metode_pembayaran = order.metode_pembayaran, ekspedisi = order.ekspedisi, 
    informasi_pengiriman = order.informasi_pengiriman)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def create_item_order(db: Session, item: schemas.ItemPesananCreate, pesanan: int):
    harga_produk = item.kuantitas * (get_product(db,item.produk).harga)
    db_item = models.item_pesanan(id_pesanan = pesanan, id_produk = item.produk, kuantitas= item.kuantitas, 
    total_harga_produk = harga_produk, notes = item.notes)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
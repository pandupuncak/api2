from sqlalchemy import Boolean, BigInteger, Date, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import column


from .database import Base




class User(Base):
    __tablename__ = "pelanggan"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    username = Column(String(100))
    tanggal_lahir = Column(Date)
    alamat = Column(String(255))
    no_telp = Column(String(20))
    status = Column(String(10), nullable=True)

class Order(Base):
    __tablename__ = "pesanan"

    id_pesanan = Column(BigInteger, primary_key=True, index=True)
    id_user = Column(BigInteger, ForeignKey("pelanggan.id"))
    nama_pemesan = Column(String(255))
    no_telepon= Column(String(20))
    alamat_pengiriman = Column(String(255))
    total_harga = Column(Integer)
    metode_pembayaran = Column(String(255))
    ekspedisi = Column(String(255))
    benefit = Column(BigInteger, ForeignKey("benefit.id_benefit"))
    status_pesanan = Column(String(255))
    informasi_pengiriman = Column(String(255))

    products = relationship("item_pesanan", back_populates="orders")

class item_pesanan(Base):
    __tablename__ = "product_orders"
    
    id_pesanan = Column(BigInteger, ForeignKey("pesanan.id_pesanan"), primary_key=True, )
    id_produk = Column(BigInteger, ForeignKey("product.product_id"), primary_key=True)
    kuantitas = Column(Integer)
    total_harga_produk = Column(Integer)
    notes = Column(Text)

    orders = relationship("Order", back_populates="products")


class Products(Base):
    __tablename__ = "product"

    product_id = Column(BigInteger, primary_key=True, index=True)
    nama_product = Column(String(255))
    harga = Column(Integer)
    deskripsi = Column(String(255))
    stok = Column(Integer)
    gambar = Column(String(255))

class Benefit(Base):
    __tablename__ = "benefit"

    id_konten = Column(BigInteger)
    id_benefit = Column(BigInteger, primary_key=True, index=True)
    nama_benefit = Column(String(255))
    deskripsi = Column(Text)
    konten = Column(String(255))
    caption = Column(String(255))
    syarat_ketentuan = Column(Text)
    diskon = Column(Integer)
    stok = Column(Integer)

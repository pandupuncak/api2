from sqlalchemy import Boolean, Column, ForeignKey, BigInteger, String, Date, Text,Integer
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Enum
from .database import Base
from sqlalchemy.orm import relationship

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

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

class Order(Base):
    __tablename__ = "pesanan"

    id_pesanan = Column(BigInteger, primary_key=True)
    id_user = Column(BigInteger, ForeignKey("pelanggan.id"))
    nama_pemesan = Column(String(255))
    no_telepon= Column(String(20), nullable=True)
    alamat_pengiriman = Column(String(255))
    total_harga = Column(Integer)
    metode_pembayaran = Column(String(255))
    ekspedisi = Column(String(255))
    id_benefit = Column(BigInteger, ForeignKey("benefit.id_benefit"), nullable=True)
    status_pesanan = Column(String(255))

    products = relationship("item_pesanan", back_populates="orders")

class item_pesanan(Base):
    __tablename__ = "product_orders"
    
    id_pesanan = Column(BigInteger, ForeignKey("pesanan.id_pesanan"), primary_key=True)
    id_produk = Column(BigInteger, ForeignKey("product.product_id"), primary_key=True)
    kuantitas = Column(Integer)
    total_harga_produk = Column(Integer)
    notes = Column(Text, nullable=True)

    orders = relationship("Order", back_populates="products")


class Product(Base):
    __tablename__ = "product"

    product_id = Column(BigInteger, primary_key=True)
    nama_product = Column(String(255))
    harga = Column(Integer)
    deskripsi = Column(String(255))
    stok = Column(Integer)
    gambar = Column(String(255))

class Benefit(Base):
    __tablename__ = "benefit"

    id_konten = Column(BigInteger)
    id_benefit = Column(BigInteger, primary_key=True)
    nama_benefit = Column(String(255))
    deskripsi = Column(Text)
    konten = Column(String(255))
    caption = Column(String(255))
    syarat_ketentuan = Column(Text)
    diskon = Column(Integer)
    syarat_poin = Column(Integer)

# class BenefitMember(Base):
#     __tablename__ = "benefitMember"

#     member_id = Column(Integer)
#     benefit_id = Column(BigInteger)
#     kuantitas = Column(Integer)
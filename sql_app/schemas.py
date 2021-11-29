from datetime import date
from typing import List, Optional

from pydantic import BaseModel

class ProdukBase(BaseModel):
    id_produk: int
    nama_produk: str
    harga: int
    deskripsi: str
    stok: int
    gambar: str

class Produk(ProdukBase):
    class Config:
        orm_mode = True

class BenefitBase(BaseModel):
    id_benefit: int
    nama: str
    poin: int
    stok: int
    deskripsi: str

class Benefit(BenefitBase):
    class Config:
        orm_mode = True

class ItemPesananBase(BaseModel):
    id_produk : int
    id_pesanan: int
    kuantitas: int
    notes: Optional[str]

class ItemPesanan(ItemPesananBase):
    total_harga_produk: int
    class Config:
        orm_mode = True

class PesananBase(BaseModel):
    id_user: int
    nama_pemesan: str
    no_telepon: int
    alamat_pengiriman: str
    metode_pembayaran: str
    ekspedisi: str
    total_harga: int = 0
    benefit : Optional[int]
    status_pesanan : str = "Accepted"

class PesananCreate(PesananBase):
    id_produk: int
    kuantitas: int
    notes: Optional[str]

class Pesanan(PesananBase):
    id: int
    class Config:
        orm_mode = True
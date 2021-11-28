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
    kuantitas: int
    notes: str

class ItemPesananCreate(ItemPesananBase):
    produk: int


class ItemPesanan(ItemPesananBase):
    id_pesanan: int
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
    informasi_pengiriman: Optional[str] 

    #Tambahin status, benefit, rincian pesanan di inherit

class PesananCreate(PesananBase):
    benefit : Optional[Benefit]

class Pesanan(PesananBase):
    id: int
    rincian_pesanan: List[ItemPesanan] = []
    total_harga: int = 0
    status_pesanan : str

    class Config:
        orm_mode = True
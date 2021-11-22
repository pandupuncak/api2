from typing import List, Optional


from pydantic import BaseModel

class produk(BaseModel):
    id_produk: int
    nama_produk: str
    harga: int
    deskripsi: str
    stok: int
    gambar: str

class Benefit(BaseModel):
    id_benefit: int
    nama: str
    poin: int
    stok: int
    deskripsi: str

class item_pesanan(BaseModel):
    id_pesanan: int
    produk: produk
    kuantitas: int
    total_harga_produk: int
    notes: str

class pesanan(BaseModel):
    id_pesanan: int
    id_user: int
    nama_pemesan: str
    no_telepon: int
    alamat_pengiriman: str
    total_harga: int
    metode_pembayaran: str
    ekspedisi: str
    benefit: Benefit
    status_pesanan: str
    informasi_pengiriman: str
   
    rincian_pesanan: List[item_pesanan]

class Status(BaseModel):
    id_pesanan: int
    status_pesanan: str


class ItemBase(BaseModel):

    title: str

    description: Optional[str] = None




class ItemCreate(ItemBase):

    pass



class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True



class UserBase(BaseModel):

    email: str




class UserCreate(UserBase):

    password: str



class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True

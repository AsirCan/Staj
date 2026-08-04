"""
Gün 16 - FastAPI Temelleri & HTTP Routing Uygulamalı Örnek Betiği
Çalıştırmak için:
    uvicorn gun16_fastapi_demo:app --reload
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

# 1. FastAPI Uygulama Nesnesi
app = FastAPI(
    title="Gün 16 - FastAPI Routing & HTTP Demo",
    description="HTTP GET, POST, PUT, DELETE metotları ve parametre kullanımı gösterimi.",
    version="1.0.0"
)

# Geçici Veritabanı Simülasyonu (Bellek İçi)
stajyer_db = [
    {"id": 1, "isim": "Ahmet Yılmaz", "departman": "Yapay Zeka", "aktif": True},
    {"id": 2, "isim": "Ayşe Kaya", "departman": "Backend Geliştirme", "aktif": True},
    {"id": 3, "isim": "Mehmet Demir", "departman": "Veri Bilimi", "aktif": False},
]

# ---------------------------------------------------------
# 1. Kök Endpoint (GET)
# ---------------------------------------------------------
@app.get("/", summary="Kök Hoşgeldin Endpoint'i")
def ana_sayfa():
    """Staj Gün 16 karşılama mesajı döner."""
    return {
        "sistem": "Staj FastAPI Sunucusu",
        "gun": 16,
        "durum": "Hazır ve Çalışıyor"
    }

# ---------------------------------------------------------
# 2. Query Parameters ile Listeleme & Filtreleme (GET)
# ---------------------------------------------------------
@app.get("/stajyerler/", summary="Stajyerleri Listele ve Filtrele")
def stajyer_listele(
    departman: Optional[str] = None,
    sadece_aktifler: bool = True,
    limit: int = 10
):
    """
    Stajyerleri departmana ve aktiflik durumuna göre filtreler.
    - **departman**: (İsteğe bağlı) Departman adı filtresi.
    - **sadece_aktifler**: Sadece aktif stajyerleri getirir (Varsayılan: True).
    - **limit**: Getirilecek maksimum sayı.
    """
    sonuclar = []
    for s in stajyer_db:
        if sadece_aktifler and not s["aktif"]:
            continue
        if departman and departman.lower() not in s["departman"].lower():
            continue
        sonuclar.append(s)
        if len(sonuclar) >= limit:
            break
            
    return {
        "toplam_bulunan": len(sonuclar),
        "veriler": sonuclar
    }

# ---------------------------------------------------------
# 3. Path Parameters ile Tekli Veri Getirme (GET)
# ---------------------------------------------------------
@app.get("/stajyerler/{stajyer_id}", summary="ID ile Stajyer Detayı Getir")
def stajyer_detay(stajyer_id: int):
    """
    Yol parametresi olarak gelen `stajyer_id` ile eşleşen kaydı döner.
    Bulunamazsa 404 hatası verir.
    """
    for s in stajyer_db:
        if s["id"] == stajyer_id:
            return {"durum": "Başarılı", "veri": s}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{stajyer_id} ID'li stajyer sistemde bulunamadı!"
    )

# ---------------------------------------------------------
# 4. POST Metodu ile Yeni Kayıt Ekleme
# ---------------------------------------------------------
class StajyerEkleRequest(BaseModel):
    isim: str
    departman: str
    aktif: bool = True

@app.post(
    "/stajyerler/", 
    status_code=status.HTTP_201_CREATED,
    summary="Yeni Stajyer Kaydı Oluştur"
)
def stajyer_ekle(yeni_stajyer: StajyerEkleRequest):
    """
    HTTP Request Body içerisinden JSON alarak yeni bir stajyer kaydı ekler.
    """
    yeni_id = max(s["id"] for s in stajyer_db) + 1 if stajyer_db else 1
    kayit = {
        "id": yeni_id,
        "isim": yeni_stajyer.isim,
        "departman": yeni_stajyer.departman,
        "aktif": yeni_stajyer.aktif
    }
    stajyer_db.append(kayit)
    return {
        "mesaj": "Stajyer başarıyla eklendi.",
        "olusturulan_kayit": kayit
    }

# ---------------------------------------------------------
# 5. DELETE Metodu ile Kayıt Silme
# ---------------------------------------------------------
@app.delete("/stajyerler/{stajyer_id}", summary="Stajyer Kaydı Sil")
def stajyer_sil(stajyer_id: int):
    """Verilen ID'ye sahip stajyer kaydını siler."""
    global stajyer_db
    ilk_uzunluk = len(stajyer_db)
    stajyer_db = [s for s in stajyer_db if s["id"] != stajyer_id]
    
    if len(stajyer_db) == ilk_uzunluk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{stajyer_id} ID'li stajyer silinemedi, çünkü bulunamadı."
        )
        
    return {"mesaj": f"{stajyer_id} ID'li stajyer başarıyla silindi."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("gun16_fastapi_demo:app", host="127.0.0.1", port=8000, reload=True)

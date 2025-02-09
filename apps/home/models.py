from apps import db
from datetime import datetime

class YemTedarikci(db.Model):
    __tablename__ = 'yem_tedarikcileri'
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(255), nullable=False)
    iletisim = db.Column(db.String(255))
    adres = db.Column(db.Text)
    aktif_mi = db.Column(db.Boolean, default=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<YemTedarikci {self.ad}>'

class Arac(db.Model):
    __tablename__ = 'araclar'
    id = db.Column(db.Integer, primary_key=True)
    plaka = db.Column(db.String(20), unique=True, nullable=False)
    arac_tipi = db.Column(db.String(100))
    kapasite = db.Column(db.Float)
    aktif_mi = db.Column(db.Boolean, default=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Arac {self.plaka}>'

class SutFabrikasi(db.Model):
    __tablename__ = 'sut_fabrikalari'
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(255), nullable=False)
    lokasyon = db.Column(db.String(255))
    gunluk_kapasite = db.Column(db.Float)
    aktif_mi = db.Column(db.Boolean, default=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SutFabrikasi {self.ad}>'

class Mustahsil(db.Model):
    __tablename__ = 'mustahsiller'
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    tc_no = db.Column(db.String(11), unique=True)
    telefon = db.Column(db.String(20))
    adres = db.Column(db.Text)
    aktif_mi = db.Column(db.Boolean, default=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Mustahsil {self.ad} {self.soyad}>'

class HesapKesimPeryodu(db.Model):
    __tablename__ = 'hesap_kesim_peryotlari'
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    baslangic_tarihi = db.Column(db.Date, nullable=False)
    bitis_tarihi = db.Column(db.Date, nullable=False)
    aktif_mi = db.Column(db.Boolean, default=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<HesapKesimPeryodu {self.ad}>'

class Kullanici(db.Model):
    __tablename__ = 'kullanicilar'
    id = db.Column(db.Integer, primary_key=True)
    kullanici_adi = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sifre_hash = db.Column(db.String(255), nullable=False)
    ad = db.Column(db.String(100))
    soyad = db.Column(db.String(100))
    rol = db.Column(db.String(50))
    aktif_mi = db.Column(db.Boolean, default=True)
    son_giris = db.Column(db.DateTime)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Kullanici {self.kullanici_adi}>'

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(20), unique=True, nullable=False)
    driver_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Vehicle {self.plate}>'
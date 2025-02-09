from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Optional

class YemTedarikciForm(FlaskForm):
    ad = StringField('Tedarikçi Adı', validators=[DataRequired(), Length(min=3, max=255)])
    iletisim = StringField('İletişim', validators=[Optional(), Length(max=255)])
    adres = StringField('Adres', validators=[Optional()])
    aktif_mi = BooleanField('Aktif mi?', default=True)

class AracForm(FlaskForm):
    plaka = StringField('Araç Plakası', validators=[DataRequired(), Length(min=6, max=20)])
    arac_tipi = SelectField('Araç Tipi', choices=[
        ('sut_toplama', 'Süt Toplama Aracı'), 
        ('nakliye', 'Nakliye Aracı'), 
        ('sogutma_tanki', 'Soğutma Tankı')
    ], validators=[DataRequired()])
    kapasite = FloatField('Kapasite (Litre)', validators=[Optional()])
    aktif_mi = BooleanField('Aktif mi?', default=True)

class SutFabrikasiForm(FlaskForm):
    ad = StringField('Fabrika Adı', validators=[DataRequired(), Length(min=3, max=255)])
    lokasyon = StringField('Lokasyon', validators=[Optional(), Length(max=255)])
    gunluk_kapasite = FloatField('Günlük Kapasite (Litre)', validators=[Optional()])
    aktif_mi = BooleanField('Aktif mi?', default=True)

class MustahsilForm(FlaskForm):
    ad = StringField('Ad', validators=[DataRequired(), Length(min=2, max=100)])
    soyad = StringField('Soyad', validators=[DataRequired(), Length(min=2, max=100)])
    tc_no = StringField('TC Numarası', validators=[Optional(), Length(min=11, max=11)])
    telefon = StringField('Telefon', validators=[Optional(), Length(max=20)])
    adres = StringField('Adres', validators=[Optional()])
    aktif_mi = BooleanField('Aktif mi?', default=True)

class HesapKesimPeryoduForm(FlaskForm):
    ad = StringField('Periyot Adı', validators=[DataRequired(), Length(min=3, max=100)])
    baslangic_tarihi = DateField('Başlangıç Tarihi', validators=[DataRequired()])
    bitis_tarihi = DateField('Bitiş Tarihi', validators=[DataRequired()])
    aktif_mi = BooleanField('Aktif mi?', default=True)

class KullaniciForm(FlaskForm):
    kullanici_adi = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    ad = StringField('Ad', validators=[Optional(), Length(max=100)])
    soyad = StringField('Soyad', validators=[Optional(), Length(max=100)])
    rol = SelectField('Rol', choices=[
        ('admin', 'Yönetici'), 
        ('kullanici', 'Kullanıcı'), 
        ('raporlama', 'Raporlama')
    ], validators=[DataRequired()])
    aktif_mi = BooleanField('Aktif mi?', default=True)
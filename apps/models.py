from apps import db
from datetime import datetime
from enum import Enum
from apps.authentication.models import Users  # noqa: F401 - Used in relationship

class AccountType(Enum):
    MILK_SUPPLIER = 'MILK_SUPPLIER'  # Süt tedarikçisi (müstahsil)
    FEED_SUPPLIER = 'FEED_SUPPLIER'  # Yem tedarikçisi
    MILK_COMPANY = 'MILK_COMPANY'    # Süt firması
    OTHER = 'OTHER'                  # Diğer

class FeedType(db.Model):
    __tablename__ = 'feed_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    unit = db.Column(db.String(20), default='KG')  # KG, TON, vs.
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.Enum(AccountType), nullable=False)
    balance = db.Column(db.Float, default=0)  # Borç (-) / Alacak (+)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class AccountTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # DEBIT/CREDIT
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    related_model = db.Column(db.String(50))  # MilkDelivery, FeedDelivery vs.
    related_id = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)
    
    account = db.relationship('Account', backref='transactions')

class Supplier(db.Model):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))

class District(db.Model):
    __tablename__ = 'districts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    villages = db.relationship('Village', backref='district', lazy=True)

class Village(db.Model):
    __tablename__ = 'villages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class MilkSupplier(db.Model):
    __tablename__ = 'milk_suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'))
    village_id = db.Column(db.Integer, db.ForeignKey('villages.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    credit_limit = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    account = db.relationship('Account', backref='milk_supplier')
    district = db.relationship('District', backref='milk_suppliers')
    village = db.relationship('Village', backref='milk_suppliers')

class MilkDelivery(db.Model):
    __tablename__ = 'milk_delivery'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('milk_suppliers.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantity = db.Column(db.Float, nullable=False)
    fat_ratio = db.Column(db.Float)
    ph_value = db.Column(db.Float)
    vehicle_plate = db.Column(db.String(20))
    driver_name = db.Column(db.String(100))
    receipt_number = db.Column(db.String(50))
    is_delivered = db.Column(db.Boolean, default=False)
    delivery_date = db.Column(db.DateTime, nullable=True)
    available_quantity = db.Column(db.Float, default=0)
    
    milk_supplier = db.relationship('MilkSupplier', backref='milk_deliveries')

    def update_available_quantity(self):
        if self.is_delivered:
            self.available_quantity = 0
        else:
            self.available_quantity = self.quantity

class FeedSupplier(db.Model):
    __tablename__ = 'feed_supplier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    account = db.relationship('Account', backref='feed_supplier')

class VehicleFeedStock(db.Model):
    __tablename__ = 'vehicle_feed_stock'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_plate = db.Column(db.String(20), nullable=False)
    feed_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, default=0)
    purchase_price = db.Column(db.Float)
    feed_supplier_id = db.Column(db.Integer, db.ForeignKey('feed_supplier.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    feed_supplier = db.relationship('FeedSupplier', backref='vehicle_stocks')

class FeedDelivery(db.Model):
    __tablename__ = 'feed_delivery'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_stock_id = db.Column(db.Integer, db.ForeignKey('vehicle_feed_stock.id'), nullable=False)
    milk_supplier_id = db.Column(db.Integer, db.ForeignKey('milk_suppliers.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(50))  # CASH/CREDIT
    delivery_date = db.Column(db.DateTime, default=datetime.now)
    notes = db.Column(db.Text)
    
    vehicle_stock = db.relationship('VehicleFeedStock', backref='deliveries')
    milk_supplier = db.relationship('MilkSupplier', backref='feed_deliveries')

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    milk_entry_type = db.Column(db.String(20), default='collection_first')  # collection_first veya delivery_first
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class MilkFactoryDelivery(db.Model):
    __tablename__ = 'milk_factory_deliveries'
    id = db.Column(db.Integer, primary_key=True)
    delivery_date = db.Column(db.DateTime, default=datetime.now)
    quantity = db.Column(db.Float, nullable=False)
    factory_name = db.Column(db.String(100), nullable=False)
    vehicle_plate = db.Column(db.String(20))
    driver_name = db.Column(db.String(100))
    receipt_number = db.Column(db.String(50))
    fat_ratio = db.Column(db.Float)  # Yağ oranı
    ph_value = db.Column(db.Float)   # pH değeri
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

class ReportTemplate(db.Model):
    __tablename__ = 'report_templates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    report_type = db.Column(db.String(20), nullable=False)  # daily, monthly, yearly
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<ReportTemplate {self.name}>'

class SavedReport(db.Model):
    """Kaydedilmiş raporlar için model"""
    __tablename__ = 'saved_reports'
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('report_templates.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    report_data = db.Column(db.JSON)  # Raporun JSON verisi
    parameters = db.Column(db.JSON)  # Rapor parametreleri
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Users tablosuna referans
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    template = db.relationship('ReportTemplate')
    user = db.relationship('Users')

class FinancialSummary(db.Model):
    """Finansal özet tablosu"""
    __tablename__ = 'financial_summaries'
    id = db.Column(db.Integer, primary_key=True)
    summary_date = db.Column(db.Date, nullable=False)
    summary_type = db.Column(db.String(20), nullable=False)  # DAILY, MONTHLY, YEARLY
    total_milk_income = db.Column(db.Float, default=0)
    total_feed_expense = db.Column(db.Float, default=0)
    total_other_expense = db.Column(db.Float, default=0)
    net_profit = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class SupplierAnalytics(db.Model):
    """Tedarikçi analiz tablosu"""
    __tablename__ = 'supplier_analytics'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('milk_suppliers.id'), nullable=False)
    analysis_date = db.Column(db.Date, nullable=False)
    total_milk_delivered = db.Column(db.Float, default=0)
    average_fat_ratio = db.Column(db.Float)
    average_ph_value = db.Column(db.Float)
    total_feed_purchased = db.Column(db.Float, default=0)
    total_credit_used = db.Column(db.Float, default=0)
    performance_score = db.Column(db.Float)  # 0-100 arası performans puanı
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    supplier = db.relationship('MilkSupplier')

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(20), unique=True, nullable=False)
    driver_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Factory(db.Model):
    __tablename__ = 'factories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class ExpenseCategory(db.Model):
    __tablename__ = 'expense_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

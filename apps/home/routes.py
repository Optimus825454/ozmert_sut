from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from apps.models import (
    MilkDelivery, MilkSupplier, FeedDelivery, Expense, Account, AccountType,
    Factory, FeedSupplier, Vehicle, FeedType, District, Village, Users, ReportTemplate,
    MilkFactoryDelivery
)
from datetime import datetime, timedelta
import json
from apps import db
from apps.home import blueprint

blueprint = Blueprint('home', __name__)

@blueprint.route('/')
@login_required
def index():
    try:
        # Son 24 saatteki süt miktarı
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        daily_milk = MilkDelivery.query.filter(
            MilkDelivery.date >= yesterday
        ).with_entities(db.func.sum(MilkDelivery.quantity)).scalar() or 0

        # Aylık yem gideri
        first_day_of_month = today.replace(day=1)
        monthly_feed = FeedDelivery.query.filter(
            FeedDelivery.delivery_date >= first_day_of_month
        ).with_entities(db.func.sum(FeedDelivery.total_amount)).scalar() or 0

        # Aktif tedarikçi sayısı
        supplier_count = MilkSupplier.query.filter_by(is_active=True).count()

        # Aylık toplam gider
        monthly_expense = Expense.query.filter(
            Expense.date >= first_day_of_month
        ).with_entities(db.func.sum(Expense.amount)).scalar() or 0

        # Son teslimatlar
        recent_deliveries = MilkDelivery.query.order_by(
            MilkDelivery.date.desc()
        ).limit(5).all()

        # Grafik verileri - Son 30 günlük süt alımı
        thirty_days_ago = today - timedelta(days=30)
        milk_data = MilkDelivery.query.filter(
            MilkDelivery.date >= thirty_days_ago
        ).with_entities(
            db.func.date(MilkDelivery.date),
            db.func.sum(MilkDelivery.quantity)
        ).group_by(
            db.func.date(MilkDelivery.date)
        ).order_by(
            db.func.date(MilkDelivery.date)
        ).all()

        milk_chart_labels = [d[0].strftime('%d.%m') for d in milk_data]
        milk_chart_data = [float(d[1]) for d in milk_data]

        return render_template('home/index.html',
                            daily_milk=daily_milk,
                            monthly_feed=monthly_feed,
                            supplier_count=supplier_count,
                            monthly_expense=monthly_expense,
                            recent_deliveries=recent_deliveries,
                            milk_chart_labels=json.dumps(milk_chart_labels),
                            milk_chart_data=json.dumps(milk_chart_data))
    except Exception as e:
        print(f"Hata: {str(e)}")  # Hatayı konsola yazdır
        import traceback
        traceback.print_exc()  # Hata stack trace'ini yazdır
        return render_template('home/page-500.html'), 500

# Süt İşlemleri
@blueprint.route('/milk-collection')
@login_required
def milk_collection():
    return render_template('home/milk-collection.html')

@blueprint.route('/milk-deliveries')
@login_required
def milk_deliveries():
    factories = Factory.query.filter_by(is_active=True).all()
    vehicles = Vehicle.query.filter_by(is_active=True).all()
    deliveries = MilkFactoryDelivery.query.order_by(MilkFactoryDelivery.delivery_date.desc()).all()
    return render_template('home/milk-delivery.html',
                         segment='milk-deliveries',
                         factories=factories,
                         vehicles=vehicles,
                         deliveries=deliveries)

@blueprint.route('/milk-suppliers')
@login_required
def milk_suppliers():
    suppliers = MilkSupplier.query.all()
    return render_template('home/milk-suppliers.html', suppliers=suppliers)

# Yem İşlemleri
@blueprint.route('/feed-stock')
@login_required
def feed_stock():
    return render_template('home/feed-stock.html')

@blueprint.route('/feed-delivery')
@login_required
def feed_delivery():
    return render_template('home/feed-delivery.html')

@blueprint.route('/feed-suppliers')
@login_required
def feed_suppliers():
    return render_template('home/feed-suppliers.html')

# Finans İşlemleri
@blueprint.route('/accounts')
@login_required
def accounts():
    return render_template('home/accounts.html')

@blueprint.route('/expenses')
@login_required
def expenses():
    return render_template('home/expenses.html')

@blueprint.route('/reports')
@login_required
def reports():
    return render_template('home/reports.html')

# Ayarlar
@blueprint.route('/settings')
@login_required
def settings():
    factories = Factory.query.all()
    feed_types = FeedType.query.all()
    feed_suppliers = FeedSupplier.query.all()
    vehicles = Vehicle.query.all()
    milk_suppliers = MilkSupplier.query.all()
    districts = District.query.all()
    users = Users.query.all()
    report_templates = ReportTemplate.query.all()
    
    return render_template('home/settings.html',
                         segment='settings',
                         factories=factories,
                         feed_types=feed_types,
                         feed_suppliers=feed_suppliers,
                         vehicles=vehicles,
                         milk_suppliers=milk_suppliers,
                         districts=districts,
                         users=users,
                         report_templates=report_templates)

@blueprint.route('/api/districts/<int:district_id>/villages')
@login_required
def get_district_villages(district_id):
    villages = Village.query.filter_by(district_id=district_id).all()
    return jsonify({
        'villages': [{'id': v.id, 'name': v.name} for v in villages]
    })

# Hata sayfaları
@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

# API Endpoints
@blueprint.route('/api/suppliers', methods=['POST'])
@login_required
def create_supplier():
    try:
        data = request.json
        
        # Önce cari hesap oluştur
        account = Account(
            name=data['name'],
            account_type=AccountType.MILK_SUPPLIER,
            balance=0
        )
        db.session.add(account)
        db.session.flush()  # ID almak için flush
        
        # Tedarikçiyi oluştur
        supplier = MilkSupplier(
            name=data['name'],
            district_id=data.get('district_id'),
            village_id=data.get('village_id'),
            phone=data.get('phone'),
            credit_limit=float(data.get('credit_limit', 0)),
            account_id=account.id,
            notes=data.get('notes'),
            is_active=data.get('is_active', 'true') == 'true'
        )
        
        db.session.add(supplier)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tedarikçi başarıyla eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/milk-deliveries/<int:id>/deliver', methods=['POST'])
@login_required
def mark_delivery_as_delivered(id):
    try:
        delivery = MilkDelivery.query.get_or_404(id)
        delivery.is_delivered = True
        delivery.delivery_date = datetime.now()
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/milk-deliveries/<int:id>', methods=['GET'])
@login_required
def get_delivery_details(id):
    try:
        delivery = MilkDelivery.query.get_or_404(id)
        
        return jsonify({
            'id': delivery.id,
            'date': delivery.date.strftime('%d.%m.%Y %H:%M'),
            'supplier': {
                'id': delivery.supplier.id,
                'name': delivery.supplier.name
            },
            'quantity': delivery.quantity,
            'fat_ratio': delivery.fat_ratio,
            'ph_value': delivery.ph_value,
            'vehicle_plate': delivery.vehicle_plate,
            'driver_name': delivery.driver_name,
            'receipt_number': delivery.receipt_number,
            'is_delivered': delivery.is_delivered,
            'delivery_date': delivery.delivery_date.strftime('%d.%m.%Y %H:%M') if delivery.delivery_date else None
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# API Endpoints - Fabrikalar
@blueprint.route('/api/factories', methods=['GET'])
@login_required
def get_factories():
    factories = Factory.query.all()
    return jsonify([{
        'id': f.id,
        'name': f.name,
        'address': f.address,
        'phone': f.phone,
        'is_active': f.is_active
    } for f in factories])

@blueprint.route('/api/factories/<int:id>', methods=['GET'])
@login_required
def get_factory(id):
    try:
        factory = Factory.query.get_or_404(id)
        return jsonify({
            'success': True,
            'id': factory.id,
            'name': factory.name,
            'address': factory.address,
            'phone': factory.phone,
            'is_active': factory.is_active
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@blueprint.route('/api/factories', methods=['POST'])
@login_required
def create_factory():
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        data = request.json
        factory = Factory(
            name=data['name'],
            address=data.get('address'),
            phone=data.get('phone'),
            is_active=True
        )
        db.session.add(factory)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Fabrika başarıyla eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/factories/<int:id>', methods=['PUT'])
@login_required
def update_factory(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        factory = Factory.query.get_or_404(id)
        data = request.json
        
        factory.name = data['name']
        factory.address = data.get('address')
        factory.phone = data.get('phone')
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Fabrika başarıyla güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/factories/<int:id>', methods=['DELETE'])
@login_required
def delete_factory(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        factory = Factory.query.get_or_404(id)
        factory.is_active = False
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Fabrika başarıyla pasife alındı'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# API Endpoints - Yem Çeşitleri
@blueprint.route('/api/feed-types', methods=['GET'])
@login_required
def get_feed_types():
    feed_types = FeedType.query.all()
    return jsonify([{
        'id': ft.id,
        'name': ft.name,
        'description': ft.description,
        'unit': ft.unit,
        'is_active': ft.is_active
    } for ft in feed_types])

@blueprint.route('/api/feed-types/<int:id>', methods=['GET'])
@login_required
def get_feed_type(id):
    try:
        feed_type = FeedType.query.get_or_404(id)
        return jsonify({
            'success': True,
            'id': feed_type.id,
            'name': feed_type.name,
            'description': feed_type.description,
            'unit': feed_type.unit,
            'is_active': feed_type.is_active
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@blueprint.route('/api/feed-types', methods=['POST'])
@login_required
def create_feed_type():
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        data = request.json
        unit = data.get('unit', 'KG')
        
        # Birim kontrolü
        if unit not in ['KG', 'ADET']:
            return jsonify({'success': False, 'message': 'Birim sadece KG veya ADET olabilir'}), 400
        
        feed_type = FeedType(
            name=data['name'],
            description=data.get('description'),
            unit=unit,
            is_active=True
        )
        db.session.add(feed_type)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Yem çeşidi başarıyla eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/feed-types/<int:id>', methods=['PUT'])
@login_required
def update_feed_type(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        feed_type = FeedType.query.get_or_404(id)
        data = request.json
        unit = data.get('unit', feed_type.unit)
        
        # Birim kontrolü
        if unit not in ['KG', 'ADET']:
            return jsonify({'success': False, 'message': 'Birim sadece KG veya ADET olabilir'}), 400
        
        feed_type.name = data['name']
        feed_type.description = data.get('description')
        feed_type.unit = unit
        feed_type.is_active = data.get('is_active', 'true') == 'true'
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Yem çeşidi başarıyla güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/feed-types/<int:id>', methods=['DELETE'])
@login_required
def delete_feed_type(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        feed_type = FeedType.query.get_or_404(id)
        feed_type.is_active = False  # Sadece yem çeşidini pasife al
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Yem çeşidi başarıyla pasife alındı'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# API Endpoints - Rapor Şablonları
@blueprint.route('/api/report-templates', methods=['GET'])
@login_required
def get_report_templates():
    templates = ReportTemplate.query.all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'description': t.description,
        'report_type': t.report_type,
        'is_active': t.is_active
    } for t in templates])

@blueprint.route('/api/report-templates/<int:id>', methods=['GET'])
@login_required
def get_report_template(id):
    template = ReportTemplate.query.get_or_404(id)
    return jsonify({
        'id': template.id,
        'name': template.name,
        'description': template.description,
        'report_type': template.report_type,
        'is_active': template.is_active
    })

@blueprint.route('/api/report-templates', methods=['POST'])
@login_required
def create_report_template():
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        data = request.json
        template = ReportTemplate(
            name=data['name'],
            description=data.get('description'),
            report_type=data.get('report_type', 'daily'),
            is_active=True
        )
        db.session.add(template)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Rapor şablonu başarıyla eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/report-templates/<int:id>', methods=['PUT'])
@login_required
def update_report_template(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        template = ReportTemplate.query.get_or_404(id)
        data = request.json
        
        template.name = data['name']
        template.description = data.get('description')
        template.report_type = data.get('report_type', template.report_type)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Rapor şablonu başarıyla güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/report-templates/<int:id>', methods=['DELETE'])
@login_required
def delete_report_template(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        template = ReportTemplate.query.get_or_404(id)
        template.is_active = False
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Rapor şablonu başarıyla pasife alındı'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# API Endpoints - Süt Tedarikçileri
@blueprint.route('/api/milk-suppliers', methods=['GET'])
@login_required
def get_milk_suppliers():
    suppliers = MilkSupplier.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'phone': s.phone,
        'district_id': s.district_id,
        'village_id': s.village_id,
        'credit_limit': s.credit_limit,
        'notes': s.notes,
        'is_active': s.is_active
    } for s in suppliers])

@blueprint.route('/api/milk-suppliers/<int:id>', methods=['GET'])
@login_required
def get_milk_supplier(id):
    try:
        supplier = MilkSupplier.query.get_or_404(id)
        return jsonify({
            'success': True,
            'id': supplier.id,
            'name': supplier.name,
            'phone': supplier.phone,
            'district_id': supplier.district_id,
            'village_id': supplier.village_id,
            'credit_limit': supplier.credit_limit,
            'notes': supplier.notes,
            'is_active': supplier.is_active
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@blueprint.route('/api/milk-suppliers', methods=['POST'])
@login_required
def create_milk_supplier():
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        data = request.json
        
        # Önce cari hesap oluştur
        account = Account(
            name=data['name'],
            account_type=AccountType.MILK_SUPPLIER,
            balance=0
        )
        db.session.add(account)
        db.session.flush()  # ID almak için flush
        
        # Tedarikçiyi oluştur
        supplier = MilkSupplier(
            name=data['name'],
            phone=data.get('phone'),
            district_id=data.get('district_id'),
            village_id=data.get('village_id'),
            credit_limit=float(data.get('credit_limit', 0)),
            account_id=account.id,
            notes=data.get('notes'),
            is_active=True
        )
        
        db.session.add(supplier)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tedarikçi başarıyla eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/milk-suppliers/<int:id>', methods=['PUT'])
@login_required
def update_milk_supplier(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        supplier = MilkSupplier.query.get_or_404(id)
        data = request.json
        
        supplier.name = data['name']
        supplier.phone = data.get('phone')
        supplier.district_id = data.get('district_id')
        supplier.village_id = data.get('village_id')
        supplier.credit_limit = float(data.get('credit_limit', 0))
        supplier.notes = data.get('notes')
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tedarikçi başarıyla güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/milk-suppliers/<int:id>', methods=['DELETE'])
@login_required
def delete_milk_supplier(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        supplier = MilkSupplier.query.get_or_404(id)
        supplier.is_active = False
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tedarikçi başarıyla pasife alındı'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# API Endpoints - Araçlar
@blueprint.route('/api/vehicles', methods=['GET'])
@login_required
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{
        'id': v.id,
        'plate': v.plate,
        'driver_name': v.driver_name,
        'is_active': v.is_active
    } for v in vehicles])

@blueprint.route('/api/vehicles/<int:id>', methods=['GET'])
@login_required
def get_vehicle(id):
    try:
        vehicle = Vehicle.query.get_or_404(id)
        return jsonify({
            'success': True,
            'id': vehicle.id,
            'plate': vehicle.plate,
            'driver_name': vehicle.driver_name,
            'is_active': vehicle.is_active
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@blueprint.route('/api/vehicles', methods=['POST'])
@login_required
def create_vehicle():
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        data = request.json
        vehicle = Vehicle(
            plate=data['plate'],
            driver_name=data.get('driver_name'),
            is_active=True
        )
        db.session.add(vehicle)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Araç başarıyla eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/vehicles/<int:id>', methods=['PUT'])
@login_required
def update_vehicle(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        vehicle = Vehicle.query.get_or_404(id)
        data = request.json
        
        vehicle.plate = data['plate']
        vehicle.driver_name = data.get('driver_name')
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Araç başarıyla güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/vehicles/<int:id>', methods=['DELETE'])
@login_required
def delete_vehicle(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        vehicle = Vehicle.query.get_or_404(id)
        vehicle.is_active = False
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Araç başarıyla pasife alındı'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# API Endpoints - Yem Tedarikçileri
@blueprint.route('/api/feed-suppliers', methods=['GET'])
@login_required
def get_feed_suppliers():
    suppliers = FeedSupplier.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'address': s.address,
        'phone': s.phone,
        'is_active': s.is_active
    } for s in suppliers])

@blueprint.route('/api/feed-suppliers/<int:id>', methods=['GET'])
@login_required
def get_feed_supplier(id):
    try:
        supplier = FeedSupplier.query.get_or_404(id)
        return jsonify({
            'success': True,
            'id': supplier.id,
            'name': supplier.name,
            'address': supplier.address,
            'phone': supplier.phone,
            'is_active': supplier.is_active
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@blueprint.route('/api/feed-suppliers', methods=['POST'])
@login_required
def create_feed_supplier():
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        data = request.json
        
        # Önce cari hesap oluştur
        account = Account(
            name=data['name'],
            account_type=AccountType.FEED_SUPPLIER,
            balance=0
        )
        db.session.add(account)
        db.session.flush()  # ID almak için flush
        
        # Yem tedarikçisini oluştur
        supplier = FeedSupplier(
            name=data['name'],
            address=data.get('address'),
            phone=data.get('phone'),
            account_id=account.id,  # Oluşturulan hesabın ID'sini kullan
            is_active=True
        )
        db.session.add(supplier)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Yem tedarikçisi başarıyla eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/feed-suppliers/<int:id>', methods=['PUT'])
@login_required
def update_feed_supplier(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        supplier = FeedSupplier.query.get_or_404(id)
        data = request.json
        
        supplier.name = data['name']
        supplier.address = data.get('address')
        supplier.phone = data.get('phone')
        supplier.is_active = data.get('is_active', 'true') == 'true'
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Yem tedarikçisi başarıyla güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/feed-suppliers/<int:id>', methods=['DELETE'])
@login_required
def delete_feed_supplier(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        supplier = FeedSupplier.query.get_or_404(id)
        supplier.is_active = False
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Yem tedarikçisi başarıyla pasife alındı'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# API Endpoints - İlçeler
@blueprint.route('/api/districts', methods=['GET'])
@login_required
def get_districts():
    districts = District.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'villages': [{
            'id': v.id,
            'name': v.name
        } for v in d.villages]
    } for d in districts])

@blueprint.route('/api/districts', methods=['POST'])
@login_required
def create_district():
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        data = request.json
        district = District(name=data['name'])
        db.session.add(district)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'İlçe başarıyla eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/districts/<int:id>', methods=['PUT'])
@login_required
def update_district(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        district = District.query.get_or_404(id)
        data = request.json
        district.name = data['name']
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'İlçe başarıyla güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# API Endpoints - Köyler
@blueprint.route('/api/villages', methods=['POST'])
@login_required
def create_village():
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        data = request.json
        village = Village(
            name=data['name'],
            district_id=data['district_id']
        )
        db.session.add(village)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Köy başarıyla eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/villages/<int:id>', methods=['PUT'])
@login_required
def update_village(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        village = Village.query.get_or_404(id)
        data = request.json
        village.name = data['name']
        village.district_id = data['district_id']
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Köy başarıyla güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# API Endpoints - Kullanıcılar
@blueprint.route('/api/users', methods=['GET'])
@login_required
def get_users():
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
        
    users = Users.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'is_superadmin': u.is_superadmin
    } for u in users])

@blueprint.route('/api/users', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        data = request.json
        user = Users(
            username=data['username'],
            email=data['email'],
            is_superadmin=data.get('is_superadmin', False)
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Kullanıcı başarıyla eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/users/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        user = Users.query.get_or_404(id)
        data = request.json
        
        user.username = data['username']
        user.email = data['email']
        user.is_superadmin = data.get('is_superadmin', user.is_superadmin)
        
        if 'password' in data:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Kullanıcı başarıyla güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/users/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    try:
        user = Users.query.get_or_404(id)
        if user.id == current_user.id:
            return jsonify({'success': False, 'message': 'Kendinizi silemezsiniz'}), 400
            
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Kullanıcı başarıyla silindi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/users/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    try:
        if not current_user.is_superadmin:
            return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
            
        user = Users.query.get_or_404(id)
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_superadmin': user.is_superadmin
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@blueprint.route('/api/milk-factory-deliveries', methods=['POST'])
@login_required
def create_milk_factory_delivery():
    try:
        data = request.get_json()
        
        # Yeni teslimat oluştur
        delivery = MilkFactoryDelivery(
            delivery_date=datetime.strptime(data['delivery_date'], '%Y-%m-%dT%H:%M'),
            factory_name=Factory.query.get(data['factory_id']).name,
            vehicle_plate=Vehicle.query.get(data['vehicle_id']).plate,
            driver_name=data['driver_name'],
            quantity=float(data['quantity']),
            fat_ratio=float(data['fat_ratio']),
            ph_value=float(data['ph_value']),
            receipt_number=data['receipt_number'],
            notes=data.get('notes', '')
        )
        
        db.session.add(delivery)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Teslimat başarıyla kaydedildi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/milk-factory-deliveries/<int:id>', methods=['GET'])
@login_required
def get_milk_factory_delivery(id):
    try:
        delivery = MilkFactoryDelivery.query.get(id)
        if not delivery:
            return jsonify({'success': False, 'message': 'Teslimat bulunamadı'})
            
        # Factory ve Vehicle ID'lerini bul
        factory = Factory.query.filter_by(name=delivery.factory_name).first()
        vehicle = Vehicle.query.filter_by(plate=delivery.vehicle_plate).first()
        
        return jsonify({
            'success': True,
            'delivery': {
                'factory_id': factory.id if factory else None,
                'delivery_date': delivery.delivery_date.strftime('%Y-%m-%dT%H:%M'),
                'receipt_number': delivery.receipt_number,
                'vehicle_id': vehicle.id if vehicle else None,
                'driver_name': delivery.driver_name,
                'quantity': delivery.quantity,
                'fat_ratio': delivery.fat_ratio,
                'ph_value': delivery.ph_value,
                'notes': delivery.notes
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/milk-factory-deliveries/<int:id>', methods=['PUT'])
@login_required
def update_milk_factory_delivery(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Bu işlem için yetkiniz yok'})
        
    try:
        delivery = MilkFactoryDelivery.query.get(id)
        if not delivery:
            return jsonify({'success': False, 'message': 'Teslimat bulunamadı'})
            
        if delivery.is_accounted:
            return jsonify({'success': False, 'message': 'Muhasebeleşmiş teslimatlar düzenlenemez'})
            
        data = request.get_json()
        
        # Verileri güncelle
        delivery.delivery_date = datetime.strptime(data['delivery_date'], '%Y-%m-%dT%H:%M')
        delivery.factory_name = Factory.query.get(data['factory_id']).name
        delivery.vehicle_plate = Vehicle.query.get(data['vehicle_id']).plate
        delivery.driver_name = data['driver_name']
        delivery.quantity = float(data['quantity'])
        delivery.fat_ratio = float(data['fat_ratio'])
        delivery.ph_value = float(data['ph_value'])
        delivery.receipt_number = data['receipt_number']
        delivery.notes = data.get('notes', '')
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Teslimat başarıyla güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blueprint.route('/api/milk-factory-deliveries/<int:id>', methods=['DELETE'])
@login_required
def delete_milk_factory_delivery(id):
    if not current_user.is_superadmin:
        return jsonify({'success': False, 'message': 'Bu işlem için yetkiniz yok'})
        
    try:
        delivery = MilkFactoryDelivery.query.get(id)
        if not delivery:
            return jsonify({'success': False, 'message': 'Teslimat bulunamadı'})
            
        if delivery.is_accounted:
            return jsonify({'success': False, 'message': 'Muhasebeleşmiş teslimatlar silinemez'})
            
        db.session.delete(delivery)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Teslimat başarıyla silindi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


from apps import create_app, db
from apps.authentication.models import Users
from werkzeug.security import generate_password_hash

def create_test_user():
    app = create_app()
    with app.app_context():
        # Önce veritabanını temizle
        db.drop_all()
        db.create_all()
        
        # Test kullanıcısı oluştur
        test_user = Users(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            is_superadmin=True
        )
        
        # Veritabanına kaydet
        db.session.add(test_user)
        db.session.commit()
        
        print("Test kullanıcısı oluşturuldu!")
        print("Kullanıcı adı: admin")
        print("Şifre: admin123")

if __name__ == '__main__':
    create_test_user() 
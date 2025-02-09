from apps import create_app, db
from apps.models import Users
from werkzeug.security import generate_password_hash

def create_superuser():
    app = create_app()
    with app.app_context():
        # Kullanıcı oluştur
        user = Users(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash('admin123')
        )
        db.session.add(user)
        db.session.commit()
        print('Süper kullanıcı oluşturuldu!')

if __name__ == '__main__':
    create_superuser() 
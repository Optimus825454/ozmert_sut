from apps import create_app, db
from apps.models import District, Village

def init_districts_and_villages():
    app = create_app()
    with app.app_context():
        # İlçeleri ekle
        hendek = District(name='Hendek')
        akyazi = District(name='Akyazı')
        db.session.add_all([hendek, akyazi])
        db.session.commit()

        # Hendek köyleri
        hendek_villages = [
            'Akova', 'Aşağıçalıca', 'Bakacak', 'Balıklı', 'Başpınar', 'Beyköy',
            'Çamlıca', 'Çobanyatak', 'Dereboğazı', 'Dikmen', 'Döngelyatak',
            'Güldibi', 'Gündoğan', 'Güney', 'Hacıkışla', 'Hamitli', 'Hantek',
            'Harmantepe', 'Hicriye', 'Hüseyinşeyh', 'İkbaliye', 'Kahraman',
            'Kalayık', 'Karadere', 'Karatoprak', 'Kargalı', 'Kazımiye', 'Kemaliye',
            'Kırktepe', 'Kocatönge', 'Kurtuluş', 'Mahmutbey', 'Muradiye',
            'Nuriye', 'Ortaköy', 'Paşaköy', 'Pınarlı', 'Sarıyer', 'Sivritepe',
            'Soğuksu', 'Süleymaniye', 'Şerefiye', 'Teke', 'Tosunlar', 'Turalı',
            'Uzuncaorman', 'Yarıca', 'Yayalar', 'Yeniköy', 'Yeşilköy', 'Yeşilvadi',
            'Yukarıçalıca'
        ]

        # Akyazı köyleri
        akyazi_villages = [
            'Alaağaç', 'Altındere', 'Bağlıca', 'Batakköy', 'Bedilkadirbey',
            'Beldibi', 'Buğdaylı', 'Çakıroğlu', 'Çengeller', 'Çınardibi',
            'Dokurcun', 'Eskibedil', 'Gebeş', 'Gökçeler', 'Güzlek', 'Hasanbey',
            'Kabakulak', 'Karapürçek', 'Kızılcık', 'Kızılcıkorman', 'Koğucuk',
            'Küçücek', 'Küçükkarapürçek', 'Küçükköy', 'Küçükorhan', 'Küçüktepe',
            'Küçükyayla', 'Küçükyongalı', 'Küçükyüreğil', 'Kumköprü', 'Kuzuluk',
            'Mansurlar', 'Ortaköy', 'Osmanbey', 'Pazarköy', 'Reşadiye',
            'Sukenarı', 'Şerefiye', 'Taşburun', 'Taşyatak', 'Uzunçınar',
            'Vakıf', 'Yağcılar', 'Yahyalı', 'Yakaköy', 'Yeniorman', 'Yukarıköy'
        ]

        # Köyleri ekle
        for village_name in hendek_villages:
            db.session.add(Village(name=village_name, district_id=hendek.id))

        for village_name in akyazi_villages:
            db.session.add(Village(name=village_name, district_id=akyazi.id))

        db.session.commit()

if __name__ == '__main__':
    init_districts_and_villages() 
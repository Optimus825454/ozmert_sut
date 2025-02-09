document.addEventListener('DOMContentLoaded', function() {
    // Yem Tedarikçisi Form Gönderimi
    const yemTedarikciForm = document.getElementById('yemTedarikciForm');
    if (yemTedarikciForm) {
        yemTedarikciForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            fetch('/yem-tedarikcisi/ekle', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.status === 'success') {
                    Swal.fire({
                        icon: 'success',
                        title: 'Başarılı!',
                        text: result.message,
                        showConfirmButton: false,
                        timer: 1500
                    });
                    // Modal'ı kapat
                    const modal = bootstrap.Modal.getInstance(document.getElementById('yemTedarikciModal'));
                    modal.hide();
                    // Listeyi yenile
                    loadYemTedarikcileri();
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Hata!',
                        text: result.message
                    });
                }
            })
            .catch(error => {
                console.error('Hata:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Sistemsel Hata',
                    text: 'İşlem sırasında bir hata oluştu.'
                });
            });
        });
    }

    // Araç Tanımlama Form Gönderimi
    const aracForm = document.getElementById('aracForm');
    if (aracForm) {
        aracForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            fetch('/arac/ekle', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.status === 'success') {
                    Swal.fire({
                        icon: 'success',
                        title: 'Başarılı!',
                        text: result.message,
                        showConfirmButton: false,
                        timer: 1500
                    });
                    // Modal'ı kapat
                    const modal = bootstrap.Modal.getInstance(document.getElementById('aracTanimlariModal'));
                    modal.hide();
                    // Listeyi yenile
                    loadAraclar();
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Hata!',
                        text: result.message
                    });
                }
            })
            .catch(error => {
                console.error('Hata:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Sistemsel Hata',
                    text: 'İşlem sırasında bir hata oluştu.'
                });
            });
        });
    }

    // Süt Fabrikası Form Gönderimi
    const sutFabrikasiForm = document.getElementById('sutFabrikasiForm');
    if (sutFabrikasiForm) {
        sutFabrikasiForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            fetch('/sut-fabrikasi/ekle', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.status === 'success') {
                    Swal.fire({
                        icon: 'success',
                        title: 'Başarılı!',
                        text: result.message,
                        showConfirmButton: false,
                        timer: 1500
                    });
                    // Modal'ı kapat
                    const modal = bootstrap.Modal.getInstance(document.getElementById('sutFabrikaTanimlariModal'));
                    modal.hide();
                    // Listeyi yenile
                    loadSutFabrikalari();
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Hata!',
                        text: result.message
                    });
                }
            })
            .catch(error => {
                console.error('Hata:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Sistemsel Hata',
                    text: 'İşlem sırasında bir hata oluştu.'
                });
            });
        });
    }

    // Liste Yükleme Fonksiyonları
    function loadYemTedarikcileri() {
        fetch('/yem-tedarikcisi/listele')
        .then(response => response.json())
        .then(data => {
            const liste = document.getElementById('yemTedarikcileriListesi');
            if (liste) {
                liste.innerHTML = ''; // Listeyi temizle
                data.forEach(tedarikci => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${tedarikci.ad}</td>
                        <td>${tedarikci.iletisim || '-'}</td>
                        <td>${tedarikci.adres || '-'}</td>
                        <td>
                            <button class="btn btn-sm btn-primary" onclick="duzenle(${tedarikci.id})">Düzenle</button>
                            <button class="btn btn-sm btn-danger" onclick="sil(${tedarikci.id})">Sil</button>
                        </td>
                    `;
                    liste.appendChild(tr);
                });
            }
        });
    }

    // Benzer fonksiyonlar diğer listeler için de eklenecek

    // İlk yükleme
    if (document.getElementById('yemTedarikcileriListesi')) {
        loadYemTedarikcileri();
    }
});
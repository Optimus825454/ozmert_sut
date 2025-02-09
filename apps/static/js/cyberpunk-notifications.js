const cyberNotify = {
    create: function(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `cyber-notification cyber-notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;

        // Stil tanımlamaları
        notification.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 15px 25px;
            border-radius: 8px;
            z-index: 9999;
            font-family: 'Tomorrow', sans-serif;
            font-size: 14px;
            min-width: 300px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            cursor: default;
            text-align: center;
        `;

        // Tip bazlı stiller
        const styles = {
            success: {
                background: 'rgba(40, 167, 69, 0.2)',
                border: '1px solid rgba(40, 167, 69, 0.5)',
                color: '#28a745',
                boxShadow: '0 0 20px rgba(40, 167, 69, 0.3)'
            },
            error: {
                background: 'rgba(220, 53, 69, 0.2)',
                border: '1px solid rgba(220, 53, 69, 0.5)',
                color: '#dc3545',
                boxShadow: '0 0 20px rgba(220, 53, 69, 0.3)'
            },
            warning: {
                background: 'rgba(255, 193, 7, 0.2)',
                border: '1px solid rgba(255, 193, 7, 0.5)',
                color: '#ffc107',
                boxShadow: '0 0 20px rgba(255, 193, 7, 0.3)'
            },
            info: {
                background: 'rgba(8, 136, 255, 0.2)',
                border: '1px solid rgba(8, 136, 255, 0.5)',
                color: '#0888ff',
                boxShadow: '0 0 20px rgba(8, 136, 255, 0.3)'
            }
        };

        Object.assign(notification.style, styles[type]);

        // Kapatma butonu stili
        const closeButton = notification.querySelector('.notification-close');
        closeButton.style.cssText = `
            background: none;
            border: none;
            color: inherit;
            font-size: 20px;
            cursor: pointer;
            padding: 0 5px;
            margin-left: 15px;
            opacity: 0.7;
            transition: opacity 0.3s ease;
        `;

        closeButton.addEventListener('mouseover', () => closeButton.style.opacity = '1');
        closeButton.addEventListener('mouseout', () => closeButton.style.opacity = '0.7');
        closeButton.addEventListener('click', () => notification.remove());

        document.body.appendChild(notification);

        // Otomatik kapanma
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, duration);
    },

    success: function(message, duration) {
        this.create(message, 'success', duration);
    },

    error: function(message, duration) {
        this.create(message, 'error', duration);
    },

    warning: function(message, duration) {
        this.create(message, 'warning', duration);
    },

    info: function(message, duration) {
        this.create(message, 'info', duration);
    }
};

// Tab değiştirme fonksiyonu
function showTab(tabId) {
    // Tüm tab içeriklerini gizle
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('show', 'active');
    });

    // Tüm tab butonlarından active sınıfını kaldır
    document.querySelectorAll('[onclick^="showTab"]').forEach(btn => {
        btn.classList.remove('active');
    });

    // Seçilen tab'ı göster
    const selectedPane = document.getElementById(tabId);
    if (selectedPane) {
        selectedPane.classList.add('show', 'active');
    }

    // Seçilen tab butonunu aktif yap
    const selectedButton = document.querySelector(`[onclick="showTab('${tabId}')"]`);
    if (selectedButton) {
        selectedButton.classList.add('active');
    }

    // URL'ye hash ekle
    window.location.hash = tabId;
}

// Sayfa yüklendiğinde URL'deki hash'e göre tab'ı göster
document.addEventListener('DOMContentLoaded', function() {
    let hash = window.location.hash.replace('#', '');
    if (hash) {
        showTab(hash);
    } else {
        const firstTab = document.querySelector('.tab-pane');
        if (firstTab) {
            showTab(firstTab.id);
        }
    }
});
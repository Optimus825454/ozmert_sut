// Navbar scroll efekti
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
});

// Dropdown menülerin kapanması
document.addEventListener('click', function(e) {
    const dropdowns = document.querySelectorAll('.dropdown-menu');
    dropdowns.forEach(dropdown => {
        if (!dropdown.contains(e.target) && !e.target.matches('.dropdown-toggle')) {
            dropdown.classList.remove('show');
        }
    });
});

// Mobil menü toggle animasyonu
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            this.classList.toggle('is-active');
        });
    }
});

// Sayfa yüklenme animasyonu
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// Aktif menü öğesini vurgulama
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');

            // Eğer dropdown içindeyse, parent dropdown'ı da aktif yap
            const dropdownParent = link.closest('.dropdown');
            if (dropdownParent) {
                const dropdownToggle = dropdownParent.querySelector('.dropdown-toggle');
                if (dropdownToggle) {
                    dropdownToggle.classList.add('active');
                }
            }
        }
    });
});

// Form validasyonu için özel fonksiyonlar
function validateForm(formElement) {
    if (!formElement) return true;

    const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('is-invalid');
            const fieldName = input.placeholder || input.name;
            alert(`Lütfen ${fieldName} alanını doldurunuz`);
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Login formu için özel validasyon
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    }
});

// Tablo sıralama fonksiyonu
const sortTable = (table, column, asc = true) => {
    if (!table) return;

    const dirModifier = asc ? 1 : -1;
    const tbody = table.querySelector('tbody');
    if (!tbody) return;

    const rows = Array.from(tbody.querySelectorAll('tr'));

    const sortedRows = rows.sort((a, b) => {
        const aCol = a.querySelector(`td:nth-child(${column + 1})`);
        const bCol = b.querySelector(`td:nth-child(${column + 1})`);
        if (!aCol || !bCol) return 0;

        const aColText = aCol.textContent.trim();
        const bColText = bCol.textContent.trim();

        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
    });

    tbody.append(...sortedRows);
};
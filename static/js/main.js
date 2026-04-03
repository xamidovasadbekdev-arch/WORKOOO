// IshTop — Main JavaScript

// =====================
// Navbar hamburger menu
// =====================
document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.getElementById('navHamburger');
    const navLinks = document.getElementById('navLinks');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function () {
            navLinks.classList.toggle('open');
            hamburger.classList.toggle('active');
        });
        // Close on outside click
        document.addEventListener('click', function (e) {
            if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('open');
                hamburger.classList.remove('active');
            }
        });
    }

    // Auto-dismiss alerts after 5s
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(120%)';
            alert.style.transition = 'all 0.3s ease';
            setTimeout(function () { alert.remove(); }, 300);
        }, 5000);
    });

    // Filter form auto-submit on select change (already in template but just in case)
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        filterForm.querySelectorAll('select').forEach(function (sel) {
            sel.addEventListener('change', function () {
                filterForm.submit();
            });
        });
    }

    // Activate form inputs styling
    document.querySelectorAll('input, select, textarea').forEach(function (el) {
        el.addEventListener('focus', function () {
            el.parentElement.classList.add('focused');
        });
        el.addEventListener('blur', function () {
            el.parentElement.classList.remove('focused');
        });
    });
});

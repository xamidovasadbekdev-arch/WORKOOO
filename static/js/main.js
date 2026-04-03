// IshTop — Main JavaScript

document.addEventListener('DOMContentLoaded', function () {

    // =====================
    // Navbar hamburger menu
    // =====================
    const hamburger = document.getElementById('navHamburger');
    const navLinks = document.getElementById('navLinks');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function () {
            navLinks.classList.toggle('open');
            hamburger.classList.toggle('active');
        });
        document.addEventListener('click', function (e) {
            if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('open');
                hamburger.classList.remove('active');
            }
        });
    }

    // =====================
    // Profile dropdown — click toggle (hover emas!)
    // =====================
    const avatarBtn = document.querySelector('.nav-avatar-btn');
    const dropdownMenu = document.querySelector('.nav-dropdown-menu');

    if (avatarBtn && dropdownMenu) {
        avatarBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            const isOpen = dropdownMenu.classList.contains('open');
            dropdownMenu.classList.toggle('open', !isOpen);
        });

        // Tashqariga bosganda yopilsin
        document.addEventListener('click', function (e) {
            if (!avatarBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
                dropdownMenu.classList.remove('open');
            }
        });

        // Dropdown ichidagi linklarga bosganda yopilsin
        dropdownMenu.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                dropdownMenu.classList.remove('open');
            });
        });
    }

    // =====================
    // Auto-dismiss alerts after 5s
    // =====================
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(120%)';
            alert.style.transition = 'all 0.4s ease';
            setTimeout(function () { alert.remove(); }, 400);
        }, 5000);
    });

    // =====================
    // Filter form auto-submit
    // =====================
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        filterForm.querySelectorAll('select').forEach(function (sel) {
            sel.addEventListener('change', function () {
                filterForm.submit();
            });
        });
    }

    // =====================
    // Form input focus styling
    // =====================
    document.querySelectorAll('input, select, textarea').forEach(function (el) {
        el.addEventListener('focus', function () {
            el.parentElement.classList.add('focused');
        });
        el.addEventListener('blur', function () {
            el.parentElement.classList.remove('focused');
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.getElementById('nav-links');
    const mobileRegionsBtn = document.getElementById('mobile-regions-btn');
    const mobileRegionsDropdown = document.getElementById('mobile-regions-dropdown');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            // Toggle the menu visibility
            navLinks.classList.toggle('hidden');
            navLinks.classList.toggle('flex');
        });
    }

    if (mobileRegionsBtn && mobileRegionsDropdown) {
        mobileRegionsBtn.addEventListener('click', (e) => {
            // Only handle click toggle on mobile (when menu is absolute/full width)
            if (window.innerWidth < 768) {
                e.preventDefault();
                mobileRegionsDropdown.classList.toggle('hidden');
            }
        });
    }
});

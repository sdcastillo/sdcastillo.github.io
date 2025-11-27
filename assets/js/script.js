/**
 * main script for the template
 * used in almost every portfolio template out there
 */

document.addEventListener('DOMContentLoaded', () => {
  // === Navbar active tab switching ===
  const navLinks = document.querySelectorAll('[data-nav-link]');
  const pages = document.querySelectorAll('[data-page]');

  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      const target = link.getAttribute('data-nav-link').toLowerCase();

      // Update active button
      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');

      // Show correct page
      pages.forEach(page => {
        page.classList.remove('active');
        if (page.getAttribute('data-page') === target) {
          page.classList.add('active');
        }
      });
    });
  });

  // === Sidebar toggle (mobile) ===
  const sidebar = document.querySelector('[data-sidebar]');
  const sidebarBtn = document.querySelector('[data-sidebar-btn]');

  if (sidebarBtn && sidebar) {
    sidebarBtn.addEventListener('click', () => {
      sidebar.classList.toggle('active');
    });
  }

  // Optional: close sidebar when clicking a nav link (mobile)
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      sidebar.classList.remove('active');
    });
  });
});

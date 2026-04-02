document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('mobile-nav-toggle');
  const backdrop = document.getElementById('mobile-nav-backdrop');
  const sidebar = document.getElementById('sidebar');

  function closeSidebar() {
    document.body.classList.remove('sidebar-open');
    if (backdrop) backdrop.classList.remove('active');
  }

  if (toggle) {
    toggle.addEventListener('click', () => {
      document.body.classList.toggle('sidebar-open');
      if (backdrop) backdrop.classList.toggle('active');
    });
  }

  if (backdrop) backdrop.addEventListener('click', closeSidebar);
  if (sidebar) {
    sidebar.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', closeSidebar);
    });
  }
});

class Navbar {

  /**
   * render(activePage) — the call used in dashboard/compiler pages.
   * activePage: 'home' | 'about' | 'compiler' | 'dashboard'
   */
  static render(activePage) {
    Navbar._inject(activePage);
    Navbar._updateAuthSection();
  }

  /**
   * init() — auto-detects active page from the current URL filename.
   */
  static init() {
    const page = window.location.pathname.split('/').pop() || 'index.html';
    let activePage = 'home';
    if (page.includes('about'))     activePage = 'about';
    else if (page.includes('compiler') || page.includes('dashboard')) activePage = 'compiler';
    else if (page.includes('login') || page.includes('signup'))       activePage = 'login';

    Navbar._inject(activePage);
    Navbar._updateAuthSection();
  }

  /** Builds and injects the <nav> element at the top of <body> */
  static _inject(activePage) {
    // Don't double-inject
    if (document.querySelector('nav.rs-nav')) return;

    const pages = [
      { id: 'home',     label: 'Home',     href: 'index.html' },
      { id: 'about',    label: 'About',    href: 'about.html' },
      { id: 'compiler', label: 'Compiler', href: 'rulescript_dashboard.html' },
    ];

    const links = pages.map(p => `
      <li>
        <a href="${p.href}" ${p.id === activePage ? 'class="active"' : ''}>
          ${p.label}
        </a>
      </li>
    `).join('');

    const nav = document.createElement('nav');
    nav.className = 'rs-nav';
    nav.innerHTML = `
      <a href="index.html" class="nav-logo">RuleScript</a>
      <ul class="nav-links">
        ${links}
        <li id="authNavItem"></li>
      </ul>
    `;

    document.body.insertBefore(nav, document.body.firstChild);
  }

  /** Swaps auth nav item based on login state */
  static _updateAuthSection() {
    const authItem = document.getElementById('authNavItem');
    if (!authItem) return;

    if (Auth.isLoggedIn()) {
      const user = Auth.getCurrentUser();
      authItem.innerHTML = `
        <span style="display:flex;align-items:center;gap:6px;">
          <a href="rulescript_dashboard.html"
             style="background:rgba(62,207,142,0.15);color:#3ecf8e;
                    padding:6px 13px;border-radius:6px;font-weight:600;font-size:13px;
                    border:1px solid rgba(62,207,142,0.3);">
            Dashboard
          </a>
          <a href="#" onclick="Navbar._logout(event)"
             style="color:var(--text-faint);font-size:12px;padding:6px 10px;border-radius:6px;"
             title="Logout ${user ? user.username : ''}">
            Logout
          </a>
        </span>
      `;
    } else {
      authItem.innerHTML = `<a href="login.html">Login / Signup</a>`;
    }
  }

  static _logout(e) {
    e.preventDefault();
    Auth.logout('index.html');
  }
}

// Auto-run on DOMContentLoaded only if Navbar.render() hasn't been called manually yet
document.addEventListener('DOMContentLoaded', () => {
  // If no nav exists yet and no manual render() was called, auto-init
  if (!document.querySelector('nav.rs-nav')) {
    Navbar.init();
  }
});

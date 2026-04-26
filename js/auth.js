class Auth {

  static getUsers() {
    return JSON.parse(localStorage.getItem('rs_users') || '[]');
  }

  static saveUsers(users) {
    localStorage.setItem('rs_users', JSON.stringify(users));
  }

  static getCurrentUser() {
    return JSON.parse(localStorage.getItem('currentUser') || 'null');
  }

  static isLoggedIn() {
    return Auth.getCurrentUser() !== null;
  }

  static signup(username, email, password) {
    if (!username || !email || !password)
      return { success: false, message: 'All fields are required.' };
    if (password.length < 6)
      return { success: false, message: 'Password must be at least 6 characters.' };

    const users = Auth.getUsers();
    if (users.some(u => u.email.toLowerCase() === email.toLowerCase()))
      return { success: false, message: 'An account with this email already exists.' };
    if (users.some(u => u.username.toLowerCase() === username.toLowerCase()))
      return { success: false, message: 'This username is already taken.' };

    const newUser = { username, email, password };
    users.push(newUser);
    Auth.saveUsers(users);
    localStorage.setItem('currentUser', JSON.stringify(newUser));
    return { success: true, message: 'Account created successfully!' };
  }

  static login(email, password) {
    if (!email || !password)
      return { success: false, message: 'Email and password are required.' };

    const user = Auth.getUsers().find(
      u => u.email.toLowerCase() === email.toLowerCase() && u.password === password
    );
    if (!user) return { success: false, message: 'Invalid email or password.' };

    localStorage.setItem('currentUser', JSON.stringify(user));
    return { success: true, message: 'Logged in successfully!' };
  }

  static logout(redirectTo = 'index.html') {
    localStorage.removeItem('currentUser');
    window.location.href = redirectTo;
  }

  /** Call on protected pages — redirects to login if not authenticated */
  static requireLogin(loginPage = 'login.html') {
    if (!Auth.isLoggedIn()) {
      const page = encodeURIComponent(window.location.pathname.split('/').pop());
      window.location.href = `${loginPage}?redirect=${page}`;
    }
  }

  /** Call on login/signup page — skips it if already logged in */
  static redirectIfLoggedIn(dest = 'rulescript_dashboard.html') {
    if (Auth.isLoggedIn()) window.location.href = dest;
  }
}

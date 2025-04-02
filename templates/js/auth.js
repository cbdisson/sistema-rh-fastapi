const API_URL = 'http://localhost:8000/api/v1';

// Verifica autenticação em todas as páginas (exceto login)
if (!window.location.pathname.includes('index.html') && !localStorage.getItem('token')) {
    window.location.href = 'index.html';
}

// Login
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;

        try {
            const response = await fetch(`${API_URL}/rh/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(senha)}`
            });

            if (!response.ok) throw new Error('Credenciais inválidas');

            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            window.location.href = 'dashboard.html';
        } catch (error) {
            document.getElementById('error-message').textContent = error.message;
        }
    });
}

// Logout
if (document.getElementById('logoutBtn')) {
    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('token');
        window.location.href = 'index.html';
    });
}

// static/core/js/auth.js

document.addEventListener('DOMContentLoaded', function() {
    // ======================
    // Конфигурационные константы
    // ======================
    const PUBLIC_PAGES = ['/', '/login/', '/register/', '/password-reset/'];
    const PROTECTED_PAGES = ['/dashboard/', '/links/', '/categories/', '/link/create_link/'];
    const TOKEN_CHECK_INTERVAL = 5 * 60 * 1000; // 5 минут
    const TOKEN_REFRESH_THRESHOLD = 10 * 60 * 1000; // 10 минут до истечения

    // ======================
    // Основные функции
    // ======================
    
    // Получение куки по имени
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        return parts.length === 2 ? parts.pop().split(';').shift() : null;
    }

    // Проверка срока действия токена
    function isTokenExpired(token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const now = Date.now();
            return now >= (payload.exp * 1000 - TOKEN_REFRESH_THRESHOLD);
        } catch {
            return true;
        }
    }

    // Обновление access token
    async function refreshToken() {
        const refreshToken = getCookie('refresh_token');
        if (!refreshToken) return false;

        try {
            const response = await fetch('/api/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                // Устанавливаем новый access token
                document.cookie = `access_token=${data.access}; path=/; max-age=3600; Secure; SameSite=Lax`;
                return true;
            }
            return false;
        } catch (error) {
            console.error('Token refresh error:', error);
            return false;
        }
    }

    // Перенаправление на страницу входа
    function redirectToLogin() {
        if (!isPublicPage()) {
            window.location.href = `/login/?next=${encodeURIComponent(window.location.pathname)}`;
        }
    }

    // Проверка публичной страницы
    function isPublicPage() {
        return PUBLIC_PAGES.some(page => window.location.pathname.startsWith(page));
    }

    // Проверка защищенной страницы
    function isProtectedPage() {
        return PROTECTED_PAGES.some(page => window.location.pathname.startsWith(page));
    }

    // Обновление интерфейса
    function updateAuthUI() {
        const authLinks = document.getElementById('auth-links');
        const nonAuthLinks = document.getElementById('non-auth-links');
        
        if (authLinks && nonAuthLinks) {
            const isAuthenticated = !!getCookie('access_token');
            authLinks.style.display = isAuthenticated ? 'block' : 'none';
            nonAuthLinks.style.display = isAuthenticated ? 'none' : 'block';
        }
    }

    // Выход из системы
    async function performLogout() {
        try {
            await fetch('/logout/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                credentials: 'include'
            });
        } finally {
            document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
            document.cookie = 'refresh_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
            window.location.href = '/login/';
        }
    }

    // Основная проверка аутентификации
    async function checkAuth() {
        const accessToken = getCookie('access_token');
        
        // Для защищенных страниц
        if (isProtectedPage() && !accessToken) {
            redirectToLogin();
            return;
        }

        // Проверка срока действия токена
        if (accessToken && isTokenExpired(accessToken)) {
            const refreshed = await refreshToken();
            if (!refreshed && isProtectedPage()) {
                performLogout();
                return;
            }
        }

        // Обновляем интерфейс
        updateAuthUI();
    }

    // ======================
    // Инициализация
    // ======================
    
    // Обработчик кнопки выхода
    document.getElementById('logout-link')?.addEventListener('click', function(e) {
        e.preventDefault();
        performLogout();
    });

    // Первоначальная проверка
    checkAuth();
    
    // Периодическая проверка
    const authInterval = setInterval(checkAuth, TOKEN_CHECK_INTERVAL);
    
    // Очистка интервала при разгрузке страницы
    window.addEventListener('beforeunload', () => {
        clearInterval(authInterval);
    });
});
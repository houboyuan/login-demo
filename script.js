// 后端API基础URL - 需要替换为你的实际部署URL
const API_BASE_URL = 'https://login-demo-1-5prv.onrender.com'; // 或你的其他部署地址

// 检查登录状态
async function checkAuthStatus() {
    const accessToken = localStorage.getItem('access_token');

    if (accessToken) {
        try {
            const response = await fetch(`${API_BASE_URL}/user`, {
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            if (response.ok) {
                const user = await response.json();
                showUserSection(user);

                // 如果是管理员，显示用户管理界面
                if (user.role === 'admin') {
                    showAdminSection(accessToken);
                }
            } else {
                localStorage.removeItem('access_token');
                showLoginSection();
            }
        } catch (error) {
            console.error('Error checking auth status:', error);
            showLoginSection();
        }
    } else {
        showLoginSection();
    }
}

// 显示登录界面
function showLoginSection() {
    document.getElementById('loginSection').classList.remove('hidden');
    document.getElementById('userSection').classList.add('hidden');
}

// 显示用户信息界面
function showUserSection(user) {
    document.getElementById('loginSection').classList.add('hidden');
    document.getElementById('userSection').classList.remove('hidden');

    document.getElementById('userName').textContent = user.name || '未知用户';
    document.getElementById('userEmail').textContent = user.email || '未知邮箱';
    document.getElementById('userProvider').textContent = `登录方式: ${user.provider || '未知'}`;

    if (user.avatar) {
        document.getElementById('userAvatar').src = user.avatar;
    }
}

// 显示管理员界面
async function showAdminSection(accessToken) {
    document.getElementById('adminSection').classList.remove('hidden');

    try {
        const response = await fetch(`${API_BASE_URL}/users`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            displayUsersList(data.users);
        }
    } catch (error) {
        console.error('Error fetching users:', error);
    }
}

// 显示用户列表
function displayUsersList(users) {
    const usersList = document.getElementById('usersList');
    usersList.innerHTML = '';

    users.forEach(user => {
        const userItem = document.createElement('div');
        userItem.className = 'user-item';
        userItem.innerHTML = `
            <img src="${user.avatar_url || ''}" alt="${user.full_name || '用户'}">
            <div class="user-item-info">
                <h4>${user.full_name || '未知用户'}</h4>
                <p>${user.email || '未知邮箱'} • ${user.provider || '未知方式'}</p>
            </div>
        `;
        usersList.appendChild(userItem);
    });
}

// GitHub登录
async function loginWithGitHub() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/github`);
        const data = await response.json();
        window.location.href = data.login_url;
    } catch (error) {
        console.error('Error initiating GitHub login:', error);
        alert('登录失败，请重试');
    }
}

// Google登录
async function loginWithGoogle() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/google`);
        const data = await response.json();
        window.location.href = data.login_url;
    } catch (error) {
        console.error('Error initiating Google login:', error);
        alert('登录失败，请重试');
    }
}

// 退出登录
function logout() {
    localStorage.removeItem('access_token');
    showLoginSection();
}

// 处理回调（在callback.html中使用）
function handleAuthCallback() {
    const urlParams = new URLSearchParams(window.location.hash.substring(1));
    const accessToken = urlParams.get('access_token');

    if (accessToken) {
        localStorage.setItem('access_token', accessToken);
        window.location.href = 'index.html';
    } else {
        console.error('No access token found in callback');
        window.location.href = 'index.html';
    }
}

// 页面加载时检查认证状态

document.addEventListener('DOMContentLoaded', checkAuthStatus);

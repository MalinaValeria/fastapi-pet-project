const login = async (url, data) => {
    try {
        return await axios.post(url, data);
    } catch (error) {
        console.error(error);
        const alert = $('#alert');
        alert.removeAttr('hidden');
        alert.text(error.response.data.detail);
        return null;
    }
}

const submitForm = async (url, data) => {
    const result = await login(url, data);

    if (result && result.status === 200) {
        window.location.replace('/');
    } else {
        console.error(`Login failed`);
    }
}

const AUTH_URL = 'http://localhost:8000/auth/login/';

const loginForm = $('#loginForm');
loginForm.on('submit', async (event) => {
    event.preventDefault();
    const loginBtn = $('#loginForm button[type="submit"]');
    loginBtn.disabled = true;
    $('#spinner').hidden = false;
    const formData = new FormData();
    formData.append('username', $('#loginForm input[type="text"]').val());
    formData.append('password', $('#loginForm input[type="password"]').val());
    try {
        await submitForm(AUTH_URL, formData);
    } catch (error) {
        console.error(`Form submission error: ${error}`);
    }
})
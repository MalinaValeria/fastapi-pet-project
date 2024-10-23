const login = async (url, data) => {
    try {
        return await axios.post(url, data);
    } catch (error) {
        console.error(error);
        const alert = document.getElementById('alert');
        alert.hidden = false;
        alert.innerText = error.response.data.detail;
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

const loginForm = document.getElementById('loginForm');
loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('username', document.querySelector('#loginForm input[type="email"]').value);
    formData.append('password', document.querySelector('#loginForm input[type="password"]').value);
    await submitForm('http://localhost:8000/auth/authorization/', formData);
})

async function logout() {
    const result = await axios.post('http://localhost:8000/auth/logout/');
    if (result && result.status === 200) {
        window.location.replace('/');
    } else {
        console.error(`Logout failed`);
    }
}
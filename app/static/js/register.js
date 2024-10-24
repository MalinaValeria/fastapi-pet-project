const handleRegistrationError = (error) => {
    console.error(error);
    const alert = $('#alert');
    alert.removeAttr('hidden');
    const errorDetails = error.response.data.detail;
    console.log(Array.isArray(errorDetails))
    if (Array.isArray(errorDetails)) {
        alert.text(errorDetails[0].msg);
        errorDetails.forEach((detail) => {
            $('#registrationForm input[name=' + detail.loc[1] + ']').addClass('border-danger');
        })
    } else {
        alert.text(errorDetails);
    }
}

const register = async (url, data) => {
    try {
        return await axios.post(url, data);
    } catch (error) {
        handleRegistrationError(error);
        return null;
    }
}

const REGISTER_URL = 'http://localhost:8000/auth/registration/';

const registerForm = $('#registrationForm');
registerForm.on('submit', async (event) => {
    event.preventDefault();
    const registerBtn = $('#registrationForm button[type="submit"]');
    const spinner = $('#spinner');
    registerBtn.prop('disabled', true);
    spinner.removeAttr('hidden');

    const formData = {
        name: $('#registrationForm input[name="name"]').val(),
        email: $('#registrationForm input[name="email"]').val(),
        password: $('#registrationForm input[name="password"]').val(),
        password_confirm: $('#registrationForm input[name="password_confirm"]').val(),
    }
    const result = await register(REGISTER_URL, formData);

    if (result && result.status === 200) {
        window.location.replace('/');
    } else {
        registerBtn.prop('disabled', false);
        spinner.attr('hidden', true);
        console.error(`Login failed`);
    }
})
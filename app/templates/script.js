document.addEventListener('DOMContentLoaded', () => {
    const clockElement = document.getElementById('clock');
    const updateClock = () => {
        const now = new Date();
        const day = now.toLocaleDateString('en-US', { weekday: 'long' });
        const time = now.toLocaleTimeString('en-US');
        clockElement.textContent = `${day}, ${time}`;
    };
    setInterval(updateClock, 1000);

    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const password = document.getElementById('password').value;
        if (password === '123') {  // Replace 'yourpassword' with the actual password
            document.querySelector('.landing-page').style.display = 'none';
            document.querySelector('.dashboard').style.display = 'flex';
        } else {
            alert('Incorrect password!');
        }
    });
});

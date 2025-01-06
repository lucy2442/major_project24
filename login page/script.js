document.addEventListener("DOMContentLoaded", () => {
    const showRegister = document.getElementById("showRegister");
    const showLogin = document.getElementById("showLogin");
    const loginForm = document.getElementById("loginForm");
    const registerCard = document.getElementById("registerCard");
    const captchaText = document.getElementById("captchaText");
    const captchaRegisterText = document.getElementById("captchaRegisterText");
    const refreshCaptchaButtons = document.querySelectorAll(".refresh-captcha");

    const generateCaptcha = () => Math.floor(1000 + Math.random() * 9000);

    const updateCaptcha = (captchaElement) => {
        captchaElement.textContent = generateCaptcha();
    };

    // Initialize captchas
    updateCaptcha(captchaText);
    updateCaptcha(captchaRegisterText);

    // Refresh captcha on button click
    refreshCaptchaButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            const captchaBox = event.target.previousElementSibling;
            updateCaptcha(captchaBox);
        });
    });

    showRegister.addEventListener("click", () => {
        loginForm.parentElement.parentElement.classList.add("d-none");
        registerCard.classList.remove("d-none");
    });

    showLogin.addEventListener("click", () => {
        registerCard.classList.add("d-none");
        loginForm.parentElement.parentElement.classList.remove("d-none");
    });

    document.getElementById("loginForm").addEventListener("submit", (e) => {
        e.preventDefault();
        const captchaInput = document.getElementById("captchaInput").value;
        if (captchaInput !== captchaText.textContent) {
            alert("Invalid Captcha");
        } else {
            alert("Login Successful!");
        }
    });

    document.getElementById("registerForm").addEventListener("submit", (e) => {
        e.preventDefault();
        const captchaRegisterInput = document.getElementById("captchaRegisterInput").value;
        const robotCheck = document.getElementById("robotCheck").checked;

        if (captchaRegisterInput !== captchaRegisterText.textContent) {
            alert("Invalid Captcha");
        } else if (!robotCheck) {
            alert("Please confirm you are not a robot.");
        } else {
            alert("Registration Successful!");
        }
    });
});

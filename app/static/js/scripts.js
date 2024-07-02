function loadPopup(popupType) {
    var url = '';
    if (popupType === 'create_user') {
        url = "/create_user_popup/";
    } else if (popupType === 'create_class') {
        url = "/create_class_popup/";
    }

    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById('popupContent').innerHTML = data;
            document.getElementById('popupContainer').style.display = 'block';
        })
        .catch(error => console.error('Error loading popup:', error));
}

function closePopup() {
    document.getElementById('popupContainer').style.display = 'none';
    document.getElementById('popupContent').innerHTML = '';
}

function togglePopup(popupId) {
    var popups = ['createUserPopup', 'createClassPopup'];
    popups.forEach(function(id) {
        if (id === popupId) {
            var popup = document.getElementById(id);
            popup.style.display = (popup.style.display === "block") ? "none" : "block";
        } else {
            document.getElementById(id).style.display = "none";
        }
    });
}

document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.querySelector('form');
    form.addEventListener('submit', (e) => {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;

        if (password !== confirmPassword) {
            e.preventDefault();
            alert('Las contraseñas no coinciden. Por favor, inténtelo de nuevo.');
        }
    });
});

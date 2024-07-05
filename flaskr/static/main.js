function toggleDropdown() {
    document.querySelector('.user-status').classList.toggle('show');
}

window.onclick = function(event) {
    if (!event.target.matches('#userStatusDropdown')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function displayImage(event) {
    var image = document.getElementById('image-preview');
    image.src = URL.createObjectURL(event.target.files[0]);
    image.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('user_status_login').style.display = 'none';

    document.getElementById('google_login').addEventListener('click', function(event) {
        event.preventDefault(); 

        window.location.href = `/google_login`;
        // fetch(`/google_login`, {
        //     method: 'GET',
        //     })
        //     .then(response => response.json())
        //     .then(data => {
        //         if (data.user != "nil") {
        //             console.log('Login success')
        //             window.location.href = `/home`;
        //         } else {
        //             console.log('Login un-success')
        //             showConfirmModal(data.message)
        //         }
        //     })
        //     .catch(error => {
        //         console.error('Error:', error);
        // });
    });

    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault(); 

        var formData = new FormData(this);

        fetch('/login_app', {
            method: 'POST',
            body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.user != "nil") {
                    console.log('Login success')
                    window.location.href = `/home`;
                } else {
                    console.log('Login un-success')
                    showConfirmModal(data.message)
                }
                
            })
            .catch(error => {
                console.error('Error:', error);
                console.log('Login un-success');
                showConfirmModal(error)
        });
    })
})

function updateLoginUI(user) {

    console.log('inside updateLoginUI')

    document.getElementById('user_status_login').style.display = 'block';
    document.getElementById('user_status_logout').style.display = 'none';
    document.getElementById("usernale_label").textContent = '@'+user;
}

function showConfirmModal(errorDiscription) {

    document.getElementById("modelDetails").textContent = errorDiscription;

    const modal = document.getElementById("confirmationModal");
    modal.style.display = "block";

    const confirmYes = document.getElementById("confirmYes");

    confirmYes.onclick = null;

    confirmYes.addEventListener('click', function() {
        modal.style.display = "none";
    });

    const closeBtn = document.getElementsByClassName("close")[0];
    closeBtn.onclick = function() {
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
}
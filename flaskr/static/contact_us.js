

document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('user_status_login').style.display = 'block';
    document.getElementById('user_status_logout').style.display = 'none';
    document.getElementById("usernale_label").textContent = '@'+userData.Username;

    document.getElementById('contact_form').addEventListener('submit', function(event) {
        event.preventDefault(); 

        var formData = new FormData(this);
        console.log("Inside send mail")
        fetch(`/send_mail`, {
            method: 'POST',
            body: formData
            })
            .then(response => response.json())
            .then(data => {
                showPopupModal("Send Email",data.message,data.status)
                clearForm()
            })
            .catch(error => {
                console.error('Error:', error);
        });

    })
})

function clearForm() {
    document.getElementById('mail-name').value = ''
    document.getElementById('recepient-email').value = ''
    document.getElementById('contact-message').value = ''
}

function showPopupModal(title,discription,status) {

    docTitle = document.getElementById("saveModalHeading")
    docMessage = document.getElementById("saveModelDetails")

    docTitle.textContent = title;
    docMessage.textContent = discription;

    if (status) {
        docTitle.style.color = "green";
        docMessage.style.color = "green";
    }

    const modal = document.getElementById("saveDataModal");
    modal.style.display = "block";

    const confirmYes = document.getElementById("saveConfirmYes");

    confirmYes.onclick = null;

    confirmYes.addEventListener('click', function() {
        modal.style.display = "none";
        if (status) {
            window.location.href = `/home`;
        }
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
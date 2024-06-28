

document.addEventListener('DOMContentLoaded', function() {
    // document.getElementById('user_status_login').style.display = 'none';

    document.getElementById('manageUserForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        var formData = new FormData(this);

        fetch('/manage_users', {
            method: 'POST',
            body: formData
            })
            .then(response => response.json())
            .then(data => {
                
                if (data.status) {
                    console.log('Signup success - Nilusha')
                    showConfirmModal("Signup Success",data.message,true)
                    // window.location.href = `/home`;
                } else {
                    console.log('Signup un-success')
                    showConfirmModal("Signup Error",data.message,false)
                }
                
            })
            .catch(error => {
                console.error('Error:', error);
                console.log('Signup un-success');
                showConfirmModal(error)
        });
    })
})

function showConfirmModal(title,discription,status) {

    docTitle = document.getElementById("modalHeading")
    docMessage = document.getElementById("modelDetails")

    docTitle.textContent = title;
    docMessage.textContent = discription;

    if (status) {
        docTitle.style.color = "green";
        docMessage.style.color = "green";
    }

    const modal = document.getElementById("confirmationModal");
    modal.style.display = "block";

    const confirmYes = document.getElementById("confirmYes");

    confirmYes.onclick = null;

    confirmYes.addEventListener('click', function() {
        modal.style.display = "none";
        if (status) {
            window.location.href = `/`;
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
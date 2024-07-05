
function updateDetails() {
    document.getElementById('ad-title').value = adDetails;
    document.getElementById('ad-price').value = adDetails;
}

document.addEventListener('DOMContentLoaded', function() {
    
    document.getElementById('user_status_login').style.display = 'block';
    document.getElementById('user_status_logout').style.display = 'none';
    document.getElementById("usernale_label").textContent = '@' + adData.UserName;
    console.log(adData.Username)

    if (adData.AdId != 0) {
        document.getElementById('ad-title').value = adData.AdTitle;
        document.getElementById('ad-category').value = adData.AdCategory;
        document.getElementById('ad-price').value = adData.AdPrice;
        document.getElementById('ad-contact').value = adData.AdContact;
        document.getElementById('ad-email').value = adData.AdEmail;
        document.getElementById('ad-specification').value = adData.AdSpecification;
        document.getElementById('ad-description').value = adData.AdDescription;

        
        var ad_buttons_element = `<button type="submit">Update Advertisement</button>
                        <button type="button" class="btn" onclick=deleteDetails()>Delete Advertisement</button>`;
        document.querySelector(`.new_ad_form`).querySelector(`.ad_button_container`).innerHTML += ad_buttons_element;
    } else {
        var ad_buttons_element = `<button type="submit">Submit Advertisement</button>`;
        document.querySelector(`.new_ad_form`).querySelector(`.ad_button_container`).innerHTML += ad_buttons_element;
    }
    

    document.getElementById('newAdForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        var formData = new FormData(this);

        if (adData.AdId == 0) {
            fetch('/submit_ad', {
                method: 'POST',
                body: formData
                })
                .then(response => response.json())
                .then(data => {
                    showErrorModal(data.title,data.message,data.status)
                    clearForm()
                })
                .catch(error => {
                    console.error('Error:', error);
                    showErrorModal('Ad Save Error','Error Occured',false)
            });
        } else {
            showConfirmModal('Update Advertisement','Are you sure you want to update this Ad?','update',formData);           
        }

    });

    const adPrice = document.getElementById('ad-price');
    const adContact = document.getElementById('ad-contact');

    adPrice.addEventListener('input', function(event) {
        let value = event.target.value;
        value = value.replace(/\D/g, '');
        event.target.value = value;
    });

    adContact.addEventListener('input', function(event) {
        let value = event.target.value;
        value = value.replace(/\D/g, '');
        event.target.value = value;
    });
});

function clearForm() {
    document.getElementById('ad-title').value = ''
    document.getElementById('ad-price').value = ''
    document.getElementById('ad-contact').value = ''
    document.getElementById('ad-email').value = ''
    document.getElementById('ad-description').value = ''
}

function deleteDetails() {
    console.log('Inside delete Ad')
    showConfirmModal('Delete Advertisement','Are you sure you want to delete this Ad?','delete','nil')
    
}

function confirmDelete() {

    fetch(`/delete_ad/${adData.AdId}`, {
        method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            showErrorModal(data.title,data.message,data.status)
            clearForm()
        })
        .catch(error => {
            console.error('Error:', error);
    });
}

function confirmUpdate(formData) {

    fetch(`/update_ad/${adData.AdId}`, {
        method: 'POST',
        body: formData
        })
        .then(response => response.json())
        .then(data => {
            showErrorModal(data.title,data.message,data.status)
            clearForm()
        })
        .catch(error => {
            console.error('Error:', error);
    });
}

function showErrorModal(title,discription,status) {

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

function showConfirmModal(modelTitle, modelDiscription,modelType,formData) {

    document.getElementById("modalHeading").textContent = modelTitle;
    document.getElementById("modelDetails").textContent = modelDiscription;

    const modal = document.getElementById("confirmationModal");
    modal.style.display = "block";

    const confirmYes = document.getElementById("confirmYes");
    const confirmNo = document.getElementById("confirmNo");

    confirmYes.onclick = null;
    confirmNo.onclick = null;

    confirmYes.addEventListener('click', function() {
        modal.style.display = "none";
        if (modelType == 'delete') {
            confirmDelete()
        } else {
            console.log("Confirm to update advertisement")
            confirmUpdate(formData)
        }
    });

    confirmNo.addEventListener('click', function() {
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



// Function to show popup message
function showMessage(message) {
    let popup = document.getElementById('popupMessage');
    let messageText = document.getElementById('messageText');
    messageText.innerText = message;
    popup.style.display = 'block';
    // Hide popup after 3 seconds
    setTimeout(() => {
        popup.style.display = 'none';
    }, 3000);
}



function updateDetails() {
    document.getElementById('ad-title').value = adDetails;
    document.getElementById('ad-price').value = adDetails;
}


// Function to handle form submission
document.addEventListener('DOMContentLoaded', function() {
    
    if (adData.AdId != 0) {
        document.getElementById('ad-title').value = adData.AdTitle;
        document.getElementById('ad-category').value = adData.AdCategory;
        document.getElementById('ad-price').value = adData.AdPrice;
        document.getElementById('ad-contact').value = adData.AdContact;
        document.getElementById('ad-email').value = adData.AdEmail;
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
                    showMessage(data.message);
                    clearForm()
                })
                .catch(error => {
                    console.error('Error:', error);
            });
        } else {
            const userConfirmed = confirm('Are you sure you want to update this Ad?');

            if (userConfirmed) {
                fetch(`/update_ad/${adData.AdId}`, {
                    method: 'POST',
                    body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        showMessage(data.message);
                        clearForm()
                    })
                    .catch(error => {
                        console.error('Error:', error);
                });
            }
        }

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
    const userConfirmed = confirm('Are you sure you want to delete this Ad?');

    if (userConfirmed) {
        fetch(`/delete_ad/${adData.AdId}`, {
            method: 'DELETE',
            })
            .then(response => {
                if (!response.ok) {
                  // Delete failed
                  response.json().then(data => {
                        showMessage(`Failed to delete device: ${data.error}`);
                    });
                }
                else {
                  // Delete successful
                  showMessage('Device deleted successfully');
                  clearTable()
                  GetAllHomeDevices()
                }
                
              })
              .catch(error => console.error('Error:', error)
            );
    }
    
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
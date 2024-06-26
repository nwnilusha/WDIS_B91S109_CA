
function updateDetails() {
    document.getElementById('ad-title').value = adDetails;
    document.getElementById('ad-price').value = adDetails;
}


// Function to handle form submission
document.addEventListener('DOMContentLoaded', function() {
    
    document.getElementById('ad-title').value = test;
        // document.getElementById('ad-category').value = adData.category;
        // document.getElementById('ad-price').value = 5000;
        // document.getElementById('ad-contact').value = adData.contact;
        // document.getElementById('ad-email').value = adData.email;
    document.getElementById('ad-description').value = "Discription asdasd";

    document.getElementById('newAdForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        var formData = new FormData(this);
        var title = document.getElementById('ad-title').value
        var price = document.getElementById('ad-price').value
        var cantact = document.getElementById('ad-contact').value
        var email = document.getElementById('ad-email').value
        var discription = document.getElementById('ad-description').value

        fetch('/submit_ad', {
            method: 'POST',
            body: formData
            })
            .then(response => response.json())
            .then(data => {
                showMessage(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });

    });
});


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
// Function to handle form submission
document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('newAdForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        var formData = new FormData(this);
        var title = document.getElementById('ad-title').value
        var discription = document.getElementById('ad-description').value

        if (title == '') {
            showMessage('Please fill title')
        } else if (discription == '') {
            showMessage('Please fill Discription')
        }

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

    })
})


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
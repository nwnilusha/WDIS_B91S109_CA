// Function to handle form submission
document.addEventListener('DOMContentLoaded', function() {
    loadAdList()
})

//function loadAdList
function loadAdList() {
    fetch('/get_ads')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            data.Results.forEach(x => {
                console.log('Inside load ad list nilusha')
                console.log(x)
                var ad_element = `<div class="ad" id=${x['AdId']}>
                                    <h2 class="adTitle">${x['AdCategory']} - ${x['AdTitle']}</h2>
                                    <h3 class="adPrice">Price: $ ${x['AdPrice']}</h3>
                                    <h3 class="adContact">Contact No: ${x['AdContact']}</h3>
                                    <h3 class="adEmail">Email: ${x['AdEmail']}</h3>
                                    <p>${x['AdDescription']}</p>
                                  </div>`;
                document.querySelector(`.ad-section`).querySelector(`.ad_container`).innerHTML += ad_element;
            });

            // Add event listeners after elements are added to the DOM
            data.Results.forEach(x => {
                document.getElementById(x['AdId']).addEventListener('click', function() {
                    console.log('Click add :' + x['AdId']);
                    const adId = x['AdId'];
        
                    fetch('/new_advertisement', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ adId: adId }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Success:', data);
                        // Navigate to the new page
                        window.location.href = `/new_advertisement?adId=${adId}`;
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                });
            });
        })
}

document.addEventListener('DOMContentLoaded', function() {
    // Event listener for the "Create New Ad" button
    document.getElementById('newAdBtn').addEventListener('click', function() {
        console.log("Inside button click event handler")
        window.location.href = "new_advertisement";
    });
})


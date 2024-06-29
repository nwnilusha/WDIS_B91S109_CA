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
            if (userData.UserRole == 'Admin') {
                data.Results.forEach(x => {
                    document.getElementById(x['AdId']).addEventListener('click', function() {
                        console.log('Click add :' + x['AdId']);
                        const adId = x['AdId'];
    
                        window.location.href = `/new_advertisement?adId=${adId}`;
                    });
                });
            }
            
        })
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('user_status_login').style.display = 'block';
    document.getElementById('user_status_logout').style.display = 'none';
    document.getElementById("usernale_label").textContent = '@'+userData.Username;
    loadAdList()
    // Event listener for the "Create New Ad" button
    document.getElementById('newAdBtn').addEventListener('click', function() {
        console.log("Inside button click event handler")
        window.location.href = "new_advertisement";
    });
})


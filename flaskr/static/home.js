//function loadAdList
function loadAdList(category) {
    const adContainer = document.querySelector('.ad-section .ad_container .ad_list');
    adContainer.innerHTML = '';
    setUIDefault()
    if (category == 'All') {
        document.getElementById('advertisement_title').textContent = "All Advertisements"
        document.getElementById('all_ads').style.color = 'green';
        document.getElementById('all_ads').style.textDecoration = 'underline';
    } else if (category == 'House') {
        document.getElementById('advertisement_title').textContent = "House Advertisements"
        document.getElementById('house_ads').style.color = 'green';
        document.getElementById('house_ads').style.textDecoration = 'underline';
    } else if (category == 'Vehicle') {
        document.getElementById('advertisement_title').textContent = "Vehicle Advertisements"
        document.getElementById('vehicle_ads').style.color = 'green';
        document.getElementById('vehicle_ads').style.textDecoration = 'underline';
    } else if (category == 'Land') {
        document.getElementById('advertisement_title').textContent = "Land Advertisements"
        document.getElementById('land_ads').style.color = 'green';
        document.getElementById('land_ads').style.textDecoration = 'underline';
    } else if (category == 'Other') {
        document.getElementById('advertisement_title').textContent = "Other Advertisements"
        document.getElementById('other_ads').style.color = 'green';
        document.getElementById('other_ads').style.textDecoration = 'underline';
    }

    fetch(`/get_ads/${category}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Data received:', data);
        if (data && data.Results) {
            data.Results.sort((a, b) => b.AdId - a.AdId);
            data.Results.forEach(x => {
                console.log('Ad:', x);
                var clickableItem = '';
                if (userData.UserRole === 'Admin' || x['UserName'] === x['logedUserName']) {
                    clickableItem = `<span class="clickable-item" data-ad-id="${x['AdId']}" style="position: absolute; top: 10px; right: 10px; cursor: pointer;">&#9193;</span>`;
                }
                
                var ad_element = `<form class="all_ads" id="allAdForm${x['AdId']}" action="/edit_advertisement" method="post">
                                    <input type="hidden" name="adId" id="adId" value="${x['AdId']}">
                                    <div class="ad" id="ad${x['AdId']}" style="position: relative;">
                                    ${clickableItem}
                                    <h2 class="adTitle">${x['AdCategory']} - ${x['AdTitle']}</h2>
                                    <div style="display: flex; justify-content: space-between;">
                                        <h3 class="adPrice">Price: <span>&#8364;</span> ${x['AdPrice']}</h3>
                                        <h3 class="adDate">Date: <span>&#128197;</span> ${x['AdDate']}</h3>
                                    </div>
                                    <h3 class="adContact">Enquire Now: <span>&#128222;</span> ${x['AdContact']} - @ [${x['UserName']}]</h3>
                                    <h3 class="adEmail"><span style="color:black;font-weight:bold">Email: </span> <span>&#128236;</span> <span style="color:blue;font-weight:normal">${x['AdEmail']}</span></h3>
                                    <h3><span style="color:black;font-weight:bold">Specification: </span><span style="color:black;font-weight:normal">${x['AdSpecification']}</span></h3>
                                    <h3><span style="color:black;font-weight:bold">Description: </span><span style="color:black;font-weight:normal">${x['AdDescription']}</span></h3>
                                    </div>
                                </form>`;
                document.querySelector('.ad-section .ad_container .ad_list').innerHTML += ad_element;
            });

            // Attach event listeners to clickable items
            document.querySelectorAll('.clickable-item').forEach(item => {
                item.addEventListener('click', function() {
                    const adId = this.getAttribute('data-ad-id');
                    const form = document.getElementById(`allAdForm${adId}`);
                    form.submit();
                });
            });
        } else {
            console.log('No results found.');
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });


}

function setUIDefault() {
    document.getElementById('advertisement_title').textContent = "Vehicle Advertisements"
        document.getElementById('all_ads').style.color = 'black';
        document.getElementById('all_ads').style.textDecoration = 'none';
        document.getElementById('house_ads').style.color = 'black';
        document.getElementById('house_ads').style.textDecoration = 'none';
        document.getElementById('vehicle_ads').style.color = 'black';
        document.getElementById('vehicle_ads').style.textDecoration = 'none';
        document.getElementById('land_ads').style.color = 'black';
        document.getElementById('land_ads').style.textDecoration = 'none';
        document.getElementById('other_ads').style.color = 'black';
        document.getElementById('other_ads').style.textDecoration = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    // Check if elements exist before accessing their properties
    var userStatusLogin = document.getElementById('user_status_login');
    var userStatusLogout = document.getElementById('user_status_logout');
    var usernameLabel = document.getElementById('usernale_label');
    var newAdBtn = document.getElementById('newAdBtn');

    if (userStatusLogin) {
        userStatusLogin.style.display = 'block';
    } else {
        console.log('Element with ID user_status_login not found');
    }

    if (userStatusLogout) {
        userStatusLogout.style.display = 'none';
    } else {
        console.log('Element with ID user_status_logout not found');
    }

    if (usernameLabel) {
        usernameLabel.textContent = '@' + userData.Username;
    } else {
        console.log('Element with ID usernale_label not found');
    }

    if (newAdBtn) {
        newAdBtn.addEventListener('click', function(event) {
            event.preventDefault();
            console.log("Inside button click event handler");
            window.location.href = "new_advertisement";
        });
    } else {
        console.log('Element with ID newAdBtn not found');
    }

    loadAdList('All');
});


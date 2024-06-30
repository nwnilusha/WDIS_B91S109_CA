//function loadAdList
function loadAdList(category) {
    const adContainer = document.querySelector('.ad-section .ad_container .ad_list');
    adContainer.innerHTML = '';
    fetch(`/get_ads/${category}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            var clickableItem = '';
            if (userData.UserRole == 'Admin') {
                clickableItem = `<span class="clickable-item" onclick="" style="position: absolute; top: 10px; right: 10px; cursor: pointer;">&#9193;</span>`;
            }
            data.Results.forEach(x => {
                console.log('Inside load ad list nilusha')
                console.log(x)
                var ad_element = `<div class="ad" id=${x['AdId']} style="position: relative;">
                                    ${clickableItem}
                                    <h2 class="adTitle">${x['AdCategory']} - ${x['AdTitle']}</h2>
                                    <div style="display: flex; justify-content: space-between;">
                                        <h3 class="adPrice">Price: $ ${x['AdPrice']}</h3>
                                        <h3 class="adDate">Date: <span>&#128197;</span> ${x['AdDate']}</h3>
                                    </div>
                                    <h3 class="adContact">Enquire Now: <span>&#128222;</span> ${x['AdContact']} - @ [${x['UserName']}]</h3>
                                    <h3 class="adEmail"><span style="color:black;font-weight:bold">Email: </span> <span>&#128236;</span> <span style="color:blue;font-weight:normal">${x['AdEmail']}</span></h3>
                                    <h3><span style="color:black;font-weight:bold">Specification: </span><span style="color:black;font-weight:normal">${x['AdSpecification']}</span></h3>
                                    <h3><span style="color:black;font-weight:bold">Discription: </span><span style="color:black;font-weight:normal">${x['AdDescription']}</span></h3>
                                </div>`;
                document.querySelector('.ad-section .ad_container .ad_list').innerHTML += ad_element;
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
    loadAdList('All')
    // Event listener for the "Create New Ad" button
    document.getElementById('newAdBtn').addEventListener('click', function(event) {
        event.preventDefault();
        console.log("Inside button click event handler")
        window.location.href = "new_advertisement";
    });
})


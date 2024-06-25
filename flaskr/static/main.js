function toggleDropdown() {
    var dropdownMenu = document.getElementById("dropdownMenu");
    dropdownMenu.classList.toggle("show");
}

window.onclick = function(event) {
    if (!event.target.matches('#userStatusDropdown')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function displayImage(event) {
    var image = document.getElementById('image-preview');
    image.src = URL.createObjectURL(event.target.files[0]);
    image.style.display = 'block';
}

//function loadAdList
function loadAdList() {
    fetch('/get_ads')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            data.Results.forEach(x => {
                console.log('Inside load ad list nilusha')
                console.log(x)
                var ad_element = '<div class="ad"><h3>"'+x['AdTitle']+'"</h3><p>"'+x['AdDescription']+'"</p></div>';
                // document.querySelector(`.ad-section`).innerHTML = document.querySelector(`.ad-section`).innerHTML + ad_element
                document.querySelector(`.ad-section`).querySelector(`.ad_container`).innerHTML = document.querySelector(`.ad-section`).querySelector(`.ad_container`).innerHTML + ad_element
            })
        })
}


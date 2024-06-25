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
                var ad_element = '<div class="ad"><h3>"'+x['AdTitle']+'"</h3><p>"'+x['AdDescription']+'"</p></div>';
                // document.querySelector(`.ad-section`).innerHTML = document.querySelector(`.ad-section`).innerHTML + ad_element
                document.querySelector(`.ad-section`).querySelector(`.ad_container`).innerHTML = document.querySelector(`.ad-section`).querySelector(`.ad_container`).innerHTML + ad_element
            })
        })
}
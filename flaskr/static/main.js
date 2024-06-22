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
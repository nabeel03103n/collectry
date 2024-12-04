drop = () => {
    dropdown = document.getElementById("select_navs")
    console.log(select_navs.value)
}

// scripts.js

document.addEventListener("DOMContentLoaded", function() {
    const contactForm = document.getElementById("contactForm");

    if (contactForm) {
        contactForm.addEventListener("submit", function(event) {
            event.preventDefault();
            alert("Thank you for contacting us!");
            contactForm.reset();  // Reset the form after submission
        });
    }
});

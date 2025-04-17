document.addEventListener("DOMContentLoaded", function () {
    console.log("Contact page loaded!");

    const form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        alert("Thank you for your message! We will get back to you soon.");
        form.reset();
    });
});

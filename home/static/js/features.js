document.addEventListener("DOMContentLoaded", function () {
    const featureCards = document.querySelectorAll(".feature-card");

    featureCards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add("show");
        }, index * 300);
    });
});

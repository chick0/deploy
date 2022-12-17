document.addEventListener("DOMContentLoaded", () => {
    /** @type {HTMLAnchorElement} */
    const burger = document.querySelector(".navbar-burger");

    burger.addEventListener("click", () => {
        /** @type {HTMLElement} */
        const target = document.getElementById(burger.dataset.target);

        burger.classList.toggle("is-active");
        target.classList.toggle("is-active");
    });
});

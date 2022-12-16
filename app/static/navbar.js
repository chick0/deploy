document.addEventListener("DOMContentLoaded", () => {
    const el = document.querySelector(".navbar-burger");

    el.addEventListener("click", () => {
        const target = document.getElementById(el.dataset.target);

        el.classList.toggle("is-active");
        target.classList.toggle("is-active");
    });
});

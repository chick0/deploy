document.addEventListener("DOMContentLoaded", () => {
    const el = document.querySelectorAll(".navbar-burger")[0];

    el.addEventListener("click", () => {
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle("is-active");
        $target.classList.toggle("is-active");
    });
});

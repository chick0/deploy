/**
 * @param {HTMLInputElement} checkbox
 */
function update_expired_field(checkbox) {
    /** @type {HTMLDivElement} */
    const field = document.querySelector("div#expired_field");

    /** @type {HTMLInputElement} */
    const at = document.querySelector("input#expired_at");

    if (checkbox.checked) {
        field.classList.remove("is-hidden");
        at.name = "expired_at";
        at.required = true;
    } else {
        field.classList.add("is-hidden");
        at.name = "-";
        at.required = false;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    /** @type {HTMLInputElement} */
    const checkbox = document.querySelector("input[type=checkbox]");

    update_expired_field(checkbox);
    checkbox.addEventListener("change", () => update_expired_field(checkbox));
});

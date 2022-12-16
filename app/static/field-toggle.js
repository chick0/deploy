document.addEventListener("DOMContentLoaded", () => {
    const expired_field = document.getElementById("expired_field");
    const expired_at = document.getElementById("expired_at");

    document.querySelector("input[type=checkbox]").addEventListener("change", (event) => {
        if (event.currentTarget.checked) {
            expired_field.classList.remove("is-hidden");
            expired_at.name = "expired_at";
            expired_at.required = true;
        } else {
            expired_field.classList.add("is-hidden");
            expired_at.name = "-";
            expired_at.required = false;
        }
    });
});

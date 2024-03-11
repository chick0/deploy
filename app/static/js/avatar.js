document.querySelectorAll("img.avatar").forEach(
    /**
     * @param {HTMLImageElement} avatar
     */
    (avatar) => {
        avatar.onerror = () => {
            avatar.src = location.origin + "/static/favicon/64.png"
        }
    }
)

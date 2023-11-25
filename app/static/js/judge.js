const judgeSelect = document.querySelector("select#judge")

judgeSelect.addEventListener("change", () => {
    location.href = `${location.pathname}?judge=${judgeSelect.value}`
})

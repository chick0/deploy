/**
 * @param {HTMLElement} element
 */
function ask_reset(element) {
    const url = element.dataset.href;

    if (confirm("해당 계정의 비밀번호를 삭제하고 임시 비밀번호로 설정하시겠습니까?")) {
        location.href = url;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("button.ask-reset").forEach((element) => {
        element.addEventListener("click", (event) => {
            // @ts-ignore
            ask_reset(event.currentTarget);
        });
    });
});

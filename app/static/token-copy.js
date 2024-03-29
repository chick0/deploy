document.addEventListener("DOMContentLoaded", () => {
    /** @type {HTMLInputElement} */
    const token = document.querySelector("input.tk-value");

    document.querySelector("button.tk-copy").addEventListener("click", () => {
        window.navigator.clipboard
            .writeText(token.value)
            .then(() => {
                alert("배포 토큰이 복사되었습니다.");
            })
            .catch(() => {
                prompt("아래의 텍스트를 복사해주세요.", token.value);
            });
    });
});

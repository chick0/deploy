/**
 * @param {string} element_id
 * @returns {string}
 */
function get_value(element_id) {
    /** @type {HTMLInputElement} */
    const input = document.querySelector(`input#${element_id}`);
    return input.value;
}

document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("button.tk-test");

    button.addEventListener("click", () => {
        if (button.classList.contains("is-loading")) {
            alert("이미 프로젝트 정보를 불러오고 있습니다. 잠시만 기다려주세요.");
            return;
        }

        button.classList.add("is-loading");

        fetch("/api/token/test", {
            method: "POST",
            headers: {
                "x-deploy-name": get_value("x-deploy-name"),
                "x-deploy-token": get_value("x-deploy-token"),
            },
        })
            .then((resp) => resp.json())
            .then((json) => {
                alert(json.message);
                button.classList.remove("is-loading");
            })
            .catch(() => {
                alert("토큰을 테스트하는 과정에서 알 수 없는 오류가 발생했습니다.");
                button.classList.remove("is-loading");
            });
    });
});

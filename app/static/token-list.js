/**
 * @param {HTMLElement} element 
 */
function on_click(element) {
    if (element.classList.contains("is-loading")) {
        alert("해당 배포 토큰을 삭제하고 있습니다. 잠시만 기다려주세요.");
        return;
    }

    element.classList.add("is-loading");

    const token_id = element.dataset.token;

    fetch(`/api/token/${token_id}`, {
        method: "DELETE"
    })
        .then((resp) => resp.json())
        .then((json) => {
            if (json.status == false) {
                element.classList.remove("is-loading");
            } else {
                document.getElementById(`token-${token_id}`).remove();
            }

            alert(json.message);
        }).catch(() => {
            alert("배포 토큰을 삭제하는 과정에서 알 수 없는 오류가 발생했습니다.");
            element.classList.remove("is-loading");
        });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll("button.tk-delete").forEach((element) => {
        element.addEventListener("click", (event) => {
            if (confirm("해당 배포 토큰을 삭제하시겠습니까?")) {
                on_click(event.currentTarget);
            }
        });
    });
});

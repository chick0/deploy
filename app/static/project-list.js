/**
 * @param {HTMLElement} element 
 */
function on_click(element) {
    if (element.classList.contains("is-loading")) {
        alert("이미 프로젝트 정보를 불러오고 있습니다. 잠시만 기다려주세요.");
        return;
    }

    element.classList.add("is-loading");

    const project_id = element.dataset.project;

    fetch(`/api/project/${project_id}`)
        .then((resp) => resp.json())
        .then((json) => {
            if (json.status == false) {
                alert(json.message);
                element.classList.remove("is-loading");
            } else {
                const payload = json.payload;
                // TODO
                console.log(payload);
            }
        }).catch(() => {
            alert("프로젝트 정보를 불러오는 과정에서 알 수 없는 오류가 발생했습니다.");
            element.classList.remove("is-loading");
        });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll("button.dp-more").forEach((element) => {
        element.addEventListener("click", (event) => {
            on_click(event.currentTarget);
        });
    });
});

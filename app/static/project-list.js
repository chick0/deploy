/**
 * @param {number} timestamp
 * @returns {string}
 */
function stamp(timestamp) {
    return new Date(timestamp * 1000).toLocaleString();
}

/**
 * @param {number} size
 * @returns {string}
 */
function size2str(size) {
    const step = 1024;
    const KB = step;
    const MB = KB * step;
    const GB = MB * step;

    if (size >= GB) {
        return (size / GB).toFixed(2) + " GB";
    } else if (size >= MB) {
        return (size / MB).toFixed(2) + " MB";
    } else if (size >= KB) {
        return (size / KB).toFixed(2) + " KB";
    } else {
        return size.toString();
    }
}

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
                const display = document.getElementById(`display-${project_id}`);
                display.innerHTML = "";

                payload.deploy_list.forEach((deploy) => {
                    const box = document.createElement("div");
                    box.classList.add("box");
                    display.appendChild(box);

                    const content = document.createElement("div");
                    content.classList.add("content", "is-medium");

                    const title = document.createElement("h5");
                    title.classList.add("title", "is-5");
                    content.appendChild(title);

                    if (payload.last_deploy === deploy.id) {
                        const using = document.createElement("span");
                        using.classList.add("tag", "is-link");
                        using.innerText = "사용중";
                        title.appendChild(using);
                        title.appendChild(document.createTextNode(" "));
                        box.scrollIntoView();
                    }

                    const is_success = document.createElement("span");

                    if (deploy.is_success === true) {
                        is_success.classList.add("tag", "is-success");
                        is_success.innerText = "성공";
                    } else if (deploy.is_success === false) {
                        is_success.classList.add("tag", "is-danger");
                        is_success.innerText = "실패";
                    } else {
                        is_success.classList.add("tag", "is-warning");
                        is_success.innerText = "배포중";
                    }

                    title.appendChild(is_success);
                    title.appendChild(document.createTextNode(" " + stamp(deploy.created_at)));

                    const subtitle = document.createElement("p");
                    subtitle.classList.add("subtitle");
                    subtitle.innerHTML = `by <b>${deploy.owner}</b>`;
                    content.appendChild(subtitle);

                    if (deploy.size !== null) {
                        const size = document.createElement("p");
                        size.innerHTML = `용량: <b>${size2str(deploy.size)}</b>`;
                        content.appendChild(size);
                    } else {
                        const size = document.createElement("p");
                        size.innerHTML = `용량: <b class="has-text-danger has-background-danger-light">파일 삭제됨</b>`;
                        content.appendChild(size);
                    }

                    if (deploy.message !== null) {
                        const message = document.createElement("pre");
                        message.innerHTML = deploy.message;
                        content.appendChild(message);
                    }

                    box.appendChild(content);

                    // Buttons
                    const buttons = document.createElement("div");
                    buttons.classList.add("buttons");
                    box.appendChild(document.createElement("hr"));
                    box.appendChild(buttons);

                    function loading_toggle() {
                        remove.classList.toggle("is-loading");
                        apply.classList.toggle("is-loading");
                    }

                    const remove = document.createElement("button");
                    remove.classList.add("button", "is-danger");
                    remove.dataset.id = deploy.id;
                    remove.innerText = "버전 삭제하기";
                    remove.addEventListener("click", (event) => {
                        if (event.currentTarget.classList.contains("is-loading")) {
                            return;
                        }

                        if (confirm("해당 버전을 삭제하시겠습니까?")) {
                            loading_toggle();
                            fetch(`/api/deploy/${deploy.id}`, {
                                method: "DELETE",
                            })
                                .then((resp) => resp.json())
                                .then((json) => {
                                    alert(json.message);
                                    loading_toggle();

                                    if (json.status === true) {
                                        box.remove();
                                    }
                                })
                                .catch(() => {
                                    alert("버전을 삭제하는 과정에서 알 수 없는 오류가 발생했습니다.");
                                    loading_toggle();
                                });
                        }
                    });

                    buttons.appendChild(remove);

                    const apply = document.createElement("button");
                    apply.classList.add("button", "is-link");
                    apply.dataset.id = deploy.id;
                    apply.innerText = "버전 적용하기";
                    apply.addEventListener("click", (event) => {
                        if (event.currentTarget.classList.contains("is-loading")) {
                            return;
                        }

                        if (confirm("해당 버전을 적용하시겠습니까?")) {
                            loading_toggle();
                            fetch(`/api/deploy/${deploy.id}`, {
                                method: "POST",
                            })
                                .then((resp) => resp.json())
                                .then((json) => {
                                    alert(json.message);
                                    element.click();
                                })
                                .catch(() => {
                                    alert("버전을 적용하는 과정에서 알 수 없는 오류가 발생했습니다.");
                                    loading_toggle();
                                });
                        }
                    });

                    if (deploy.size !== null) {
                        buttons.appendChild(apply);
                    }

                    display.appendChild(box);
                });

                element.classList.remove("is-loading");
            }
        })
        .catch(() => {
            alert("프로젝트 정보를 불러오는 과정에서 알 수 없는 오류가 발생했습니다.");
            element.classList.remove("is-loading");
        });
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("button.dp-more").forEach((element) => {
        element.addEventListener("click", (event) => {
            on_click(event.currentTarget);
        });
    });
});

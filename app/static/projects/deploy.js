/**
 * @param {number} size
 * @returns {string}
 */
function size2str(size) {
    const step = 1024
    const KB = step
    const MB = KB * step
    const GB = MB * step

    if (size >= GB) {
        return (size / GB).toFixed(2) + " GB"
    } else if (size >= MB) {
        return (size / MB).toFixed(2) + " MB"
    } else if (size >= KB) {
        return (size / KB).toFixed(2) + " KB"
    } else {
        return size.toString()
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("button.js-is-apply").forEach((button) => {
        button.addEventListener("click", (e) => {
            let x = e.currentTarget
            let deploy_id = x.dataset.deploy

            if (confirm("해당 버전을 적용하시겠습니까?")) {
                fetch(`/api/deploy/${deploy_id}`, {
                    method: "POST",
                })
                    .then((resp) => resp.json())
                    .then((json) => {
                        alert(json.message)
                        location.reload()
                    })
                    .catch(() => {
                        alert("버전을 적용하는 과정에서 알 수 없는 오류가 발생했습니다.")
                    })
            }
        })
    })

    document.querySelectorAll("button.js-is-delete").forEach((button) => {
        button.addEventListener("click", (e) => {
            let x = e.currentTarget
            let deploy_id = x.dataset.deploy

            if (confirm("해당 버전을 삭제하시겠습니까?")) {
                fetch(`/api/deploy/${deploy_id}`, {
                    method: "DELETE",
                })
                    .then((resp) => resp.json())
                    .then((json) => {
                        alert(json.message)
                        location.reload()
                    })
                    .catch(() => {
                        alert("버전을 삭제하는 과정에서 알 수 없는 오류가 발생했습니다.")
                    })
            }
        })
    })

    document.querySelectorAll("button.js-is-tree").forEach((button) => {
        button.addEventListener("click", (e) => {
            let x = e.currentTarget
            let deploy_id = x.dataset.deploy

            fetch(`/api/deploy/${deploy_id}/tree`)
                .then((resp) => resp.json())
                .then((json) => {
                    if (json.status === true) {
                        const display = document.createElement("div")
                        display.className = "card p-3 mt-3"

                        json.payload.members.forEach((member) => {
                            const p = document.createElement("p")
                            p.className = "mb-0"

                            const b = document.createElement("b")
                            b.style.minWidth = "75px"
                            b.style.display = "inline-block"

                            if (member.is_dir) {
                                b.innerText = " "
                            } else {
                                b.innerText = size2str(member.size)
                            }

                            p.appendChild(b)
                            p.appendChild(document.createTextNode(member.name))

                            display.appendChild(p)
                        })

                        const total_size = document.createElement("p")
                        total_size.className = "mb-0"
                        total_size.innerHTML = `<b>= ${size2str(json.payload.total_size)}</b>`
                        display.appendChild(total_size)

                        const card = document.getElementById(`card-body-${deploy_id}`)
                        card.appendChild(display)

                        x.disabled = true
                    } else {
                        alert(json.message)
                    }
                })
                .catch(() => {
                    alert("파일의 세부 정보를 불러오는 과정에서 알 수 없는 오류가 발생했습니다.")
                })
        })
    })
})

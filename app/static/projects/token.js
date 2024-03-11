document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("button.as-create").addEventListener("click", (e) => {
        const name = e.currentTarget.dataset.name

        Swal.fire({
            html: `<iframe class="w-100" height="500px" src="/token/create/${name}"></iframe>`,
            showConfirmButton: false,
            allowOutsideClick: false,
            allowEscapeKey: false,
            width: "600px",
        })
    })

    document.querySelectorAll("button.as-delete").forEach((button) => {
        button.addEventListener("click", (e) => {
            const id = e.currentTarget.dataset.id

            Swal.fire({
                icon: "question",
                text: "해당 배포 토큰을 삭제하시겠습니까?",
                showCancelButton: true,
                confirmButtonText: "네",
                cancelButtonText: "아니요",
            }).then((result) => {
                if (result.isConfirmed) {
                    lock()
                    fetch(`/token/${id}`, {
                        method: "DELETE",
                    })
                        .then(async (resp) => {
                            const text = await resp.text()

                            if (resp.status == 200) {
                                Swal.fire({
                                    icon: "success",
                                    text: text,
                                }).then(() => {
                                    location.reload()
                                })
                            } else {
                                Swal.fire({
                                    icon: "error",
                                    text: text,
                                })
                            }
                        })
                        .catch(fetchFail)
                }
            })
        })
    })
})

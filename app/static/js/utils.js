function lock() {
    Swal.fire({
        icon: "info",
        text: "요청 사항을 처리하고 있습니다",
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false,
        didOpen: () => {
            Swal.showLoading()
        },
    })
}

function fetchFail() {
    alert("서버와의 통신에 실패했습니다. (현재 기기의 네트워크 상태가 오프라인이거나 서버에서 문제가 발생했습니다.)")
    Swal.close()
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".copy").forEach((button) => {
        button.addEventListener("click", (e) => {
            const text = e.currentTarget.dataset.text

            navigator.clipboard
                .writeText(text)
                .then(() => {
                    Swal.fire({
                        icon: "success",
                        text: "복사되었습니다!",
                        confirmButtonText: "확인",
                        timerProgressBar: true,
                        timer: 3000,
                    })
                })
                .catch(() => {
                    Swal.fire({
                        icon: "info",
                        text: "아레 텍스트를 복사해주세요.",
                        input: "text",
                        confirmButtonText: "확인",
                        inputAttributes: {
                            id: "copy-v-input",
                        },
                        didOpen: () => {
                            document.getElementById("copy-v-input").value = text
                            document.getElementById("copy-v-input").focus()
                        },
                    })
                })
        })
    })
})

function setStep(step) {
    document.querySelectorAll(".step").forEach((div) => {
        div.classList.add("d-none")
    })

    document.getElementById(step).classList.remove("d-none")
}

function setMessage(message) {
    document.querySelector("#step3 > .lead").innerHTML = message
}

let reloadRequired = false

document.getElementById("expired_switch").addEventListener("change", () => {
    document.getElementById("exp-display").classList.toggle("d-none")
})

document.querySelector(".as-next").addEventListener("click", () => {
    let form = new FormData()
    form.append("name", name)

    if (document.getElementById("expired_switch").checked) {
        form.append("expired_at", document.querySelector("input#expired_date").value + " " + document.querySelector("input#expired_time").value)
    }

    setStep("step2")

    fetch("/token/create", {
        method: "POST",
        body: form,
    })
        .then(async (resp) => {
            const text = await resp.text()
            if (resp.status == 201) {
                setStep("step4")
                reloadRequired = true
                document.querySelector("#token").value = text
            } else {
                setStep("step3")
                setMessage(text)
            }
        })
        .catch(() => {
            setStep("step3")
            setMessage("토큰 생성 과정에서 오류가 발생했습니다.<br>- 현재 기기가 오프라인 상태이거나 서버 문제가 발생했습니다.")
        })
})

document.querySelectorAll(".as-close").forEach((button) => {
    button.addEventListener("click", () => {
        if (reloadRequired === true) {
            window.parent.location.reload()
        } else {
            window.parent.Swal.close()
        }
    })
})

document.querySelector("#token").addEventListener("click", (e) => {
    navigator.clipboard.writeText(e.currentTarget.value).then(() => {
        alert("복사되었습니다.")
    })
})

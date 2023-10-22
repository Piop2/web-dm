const socket = io("ws://192.168.43.202:5000")
let latestText = ""

socket.on('disconnect', function(){
    const inputBox = document.getElementById("input-box")
    inputBox.disabled = true
    latestText = inputBox.value
    inputBox.value = ""
    inputBox.placeholder = "연결중..."
})

socket.on("enable_message", () =>{
    const inputBox = document.getElementById("input-box")
    inputBox.disabled = false
    inputBox.value = latestText
    inputBox.placeholder = "메시지 보내기..."
})


socket.on("message", (data) => {
    const container = document.getElementById("msg-container")
    let taskScroll = false;
    if (container.offsetHeight + container.scrollTop === container.scrollHeight) {
        taskScroll = true
    }
    addMessageElement(container, data["message"], "left", data["isSystem"])
    if (taskScroll) {
        scrollToEnd(container)
    }
})

function sendMessage() {
    if(window.event.keyCode===13){
        const inputBox = document.getElementById("input-box")
        const message = inputBox.value
        if (!message) {
            return null
        }
        inputBox.value = ""

        const container = document.getElementById("msg-container")

        addMessageElement(container, message, "right")
        scrollToEnd(container)

        socket.emit("message", message)
    }
    return null
}

function addMessageElement(container, message, direction="right", is_system=false) {
    const msgContainer = document.createElement("div")
    msgContainer.className += "message "
    if (is_system) {
        msgContainer.className += "system"
    }
    else {
        msgContainer.className += `msg-${direction}`
    }
    const msgBox = document.createElement("div")

    msgBox.innerHTML = message
    msgContainer.appendChild(msgBox)
    container.appendChild(msgContainer)
}

function scrollToEnd(container) {
    container.scrollTop = container.scrollHeight
}

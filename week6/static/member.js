// 頁面載入GET messages
loadMessages();
// task 5 POST message
const messageForm = document.getElementById("message-form");

if (messageForm) {    
    messageForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const messageArea = document.getElementById("input-content");
        const messageContent = document.getElementById("input-content").value.trim();
        const apiCreateMessageURL = '/api/message';
        try {
            const response = await fetch(apiCreateMessageURL, {
                method: 'POST',
                headers: {
                    'content-type': 'application/json'
                },
                body: JSON.stringify({content:messageContent})
            });
            if (!response.ok) {
                throw new Error(`Server error:${response.status}`);
            }
            const data = await response.json();
            // 載入並渲染message
            loadMessages();
            // 清空輸入框
            messageArea.value = '';
        } catch (error) {
            console.error("發生錯誤：", error);
            alert("留言失敗");
        }
    });
}

// task 5 GET message render function
async function loadMessages() {
    try {
        const response = await fetch('/api/message', { method: 'GET' });
        if (!response.ok) {
            throw new Error(`Server error:${response.status}`);
        }
        const responseData = await response.json();
        renderMessages(responseData.data);
    } catch (error) {
        console.error("發生錯誤:", error);
        alert("取得留言失敗");
    }
}

// render messages
async function renderMessages(msgs) {
    const messages = document.querySelector(".messages");
    messages.replaceChildren();
    // loop渲染每一則訊息
    for(let i = 0; i < msgs.length; i++) {
        const msg = await createMessageElement(msgs[i]);
        messages.appendChild(msg);
    }
}

// 建立message
async function createMessageElement(msg) {
    const messageElement = document.createElement("div");
    messageElement.className = "message";
    
    const msgUserName = document.createElement("span");
    msgUserName.className = "message-name";
    msgUserName.textContent = msg.name + ":";

    const msgContent = document.createElement("span");
    msgContent.textContent = msg.content;

    messageElement.appendChild(msgUserName);
    messageElement.appendChild(msgContent);

    return(messageElement);
}
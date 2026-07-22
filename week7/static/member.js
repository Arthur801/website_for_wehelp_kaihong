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
            if (!data.ok) {
                throw new Error("後端建立留言失敗");
            }
            // 載入並渲染message
            await loadMessages();
            // 清空輸入框
            messageArea.value = '';
        } catch (error) {
            console.error("發生錯誤：", error);
            alert("留言失敗");
        }
    });
}

// week 7 task 1 監測token btn 有沒有被按下
const tokenBtn = document.getElementById("create-token");
if (tokenBtn) {
    tokenBtn.addEventListener('click', async function() {
        const userToken = await sendToken();
        if(userToken===false) {
            console.log("建立token失敗");
        }
        else {
            // 建立token element
            renderToken(userToken);
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
        if (responseData.error) {
            throw new Error(`Server error:${response.status}`);
        }
        await renderMessages(responseData.data);
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

    // task 6 if msg.self === true, add delete button

    if (msg.self === true) {
        const msgDelBtn = document.createElement("button");
        msgDelBtn.type = "button";
        msgDelBtn.textContent = 'X';

        msgDelBtn.addEventListener("click", async () => {
            const delMsgConfirmed = confirm("你確定要刪除這則留言嗎?");

            if (!delMsgConfirmed) {
                return;
            }

            await delMessage(msg.id);
        });

        messageElement.appendChild(msgDelBtn);
    }


    return(messageElement);
}

// delete message
async function delMessage(messageID) {
    try {
        // 通知後端刪除資料庫裡的留言
        const response = await fetch(`/api/message/${messageID}`, { method: 'DELETE' });
        if (!response.ok) {
            throw new Error(`Server error:${response.status}`);
        }
        const responseData = await response.json();

        if (!responseData.ok) {
            throw new Error("後端刪除失敗");
        }
        // 重新渲染留言
        await loadMessages();
    } catch(error) {
        console.error("刪除留言失敗:", error);
        alert("刪除留言失敗");
    } 
}

// week 7 task 1
// 把後端生成的token傳遞到前端
async function sendToken() {
    try {
        // fetch /api/token
        const response = await fetch("api/token", { method : 'PUT' });
        if(!response.ok) {
            throw new Error(`Server error:${response.status}`);
        }

        const responseData = await response.json();
        if(!responseData.ok) {
            console.log(response);
            throw new Error("後端建立token失敗")
        }
        return responseData.token;

    } catch(error) {
        console.log("建立token失敗:", error);
        alert("建立token失敗")
        return false;
    }
}

async function renderToken(token) {
    try {
        const tokenContainer = document.querySelector(".token");
        tokenContainer.replaceChildren();
        const tokenElement = document.createElement("span");
        tokenElement.textContent = token;
        tokenContainer.appendChild(tokenElement);
    } catch(error) {
        console.log("前端建立token element 失敗")
        alert("顯示token失敗")
    } 
}
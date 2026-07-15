// 頁面載入GET messages


// task 5 POST message
const messageForm = document.getElementById("message-form");

if (messageForm) {    
    messageForm.addEventListener('submit', async function(event) {
        event.preventDefault();
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
            // 要再加上渲染成功留言的member page
            alert("成功留言",data);
        } catch (error) {
            console.error("發生錯誤：", error);
            alert("留言失敗");
        }
    });
}

// task 5 GET message render function
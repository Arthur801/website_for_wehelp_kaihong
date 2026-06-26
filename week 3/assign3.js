// 取得資料
const SITE = "https://cwpeng.github.io/test"
// 基本資料
let attrs = fetch("https://cwpeng.github.io/test/assignment-3-1")
    .then((response) => response.json())
    .then(data => data.rows)
    .catch((error) => {
        console.log(`Error: ${error}`);
    });
// 圖片資料
let attrsPicture = fetch("https://cwpeng.github.io/test/assignment-3-2")
    .then((response) => response.json())
    .then(data => data.rows)
    .catch((error) => {
        console.log(`Error: ${error}`);
    });
// 合併資料
Promise.all([attrs, attrsPicture])
    .then(([attractions, pictures]) => {
        for(let attr of attractions) {
            let picture = pictures.find(picture => picture.serial === attr.serial);
            const firstImage = picture.pics.match("/.*?\.jpg")[0];
            attr.pic = firstImage;
            console.log(attr);
        }
        // 顯示bar
        const bars = document.querySelector(".bars");
        for(let i = 0; i < 3; i++) {
            const bar = createBar(attractions[i]);
            bars.appendChild(bar);
        }
        // 顯示block
        const contentBlocks = document.querySelector(".content-blocks");
        for(let i = 0; i < 10; i++) {
            const block = createBlock(attractions[3+i]);
            contentBlocks.appendChild(block);   
        }
        

        // task 4
        let currentIdx = 13;
        const loadBtn = document.querySelector("#loadBtn");
        // 監聽loadBtn
        loadBtn.addEventListener("click", () => {
            let maxIdx = currentIdx+10;
            if(maxIdx >= attractions.length) {
                maxIdx = attractions.length;
            }
            for(let i = currentIdx; i < maxIdx; i++) {
                const loadBlock = createBlock(attractions[i]);
                contentBlocks.appendChild(loadBlock);
            }
            currentIdx += 10;
            if(maxIdx == attractions.length) {
                loadBtn.style.display = "none";
            }
        });
    });




function createBar(attraction) {
    const bar = document.createElement("div");
    bar.className = "bar";

    // img
    const barImg = document.createElement("img");
    barImg.src = `${SITE}${attraction.pic}`;
    barImg.alt = attraction.sname;

    // text
    const barText = document.createElement("p");
    barText.className = "bar-text";
    barText.textContent = attraction.sname;

    bar.appendChild(barImg);
    bar.appendChild(barText);

    return bar;
}

function createBlock(attraction) {
    const block = document.createElement("div");
    block.className = "block";

    // img
    const blockImg = document.createElement("img");
    blockImg.src = `${SITE}${attraction.pic}`;
    blockImg.alt = attraction.sname;

    // star
    const star = document.createElement("span");
    star.className = "star";
    star.textContent = "⭐️"

    // block text
    const blockText = document.createElement("div");
    blockText.className = "block-text";
    blockText.textContent = attraction.sname;

    block.appendChild(blockImg);
    block.appendChild(star);
    block.appendChild(blockText);
    
    return block;
}
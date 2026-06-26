// 取得資料
let attrs = fetch("https://cwpeng.github.io/test/assignment-3-1")
    .then((response) => response.json())
    .then(data => data.rows)
    .catch((error) => {
        console.log(`Error: ${error}`);
    });
let attrsPicture = fetch("https://cwpeng.github.io/test/assignment-3-2")
    .then((response) => response.json())
    .then(data => data.rows)
    .catch((error) => {
        console.log(`Error: ${error}`);
    });

// 合併資料
Promise.all([attrs, attrsPicture])
    .then(([attractions, pictures]) => {
        // console.log(attractions);
        for(let attr of attractions) {
            let picture = pictures.find(picture => picture.serial === attr.serial);
            const firstImage = picture.pics.match("/.*?\.jpg")[0];
            attr.pic = firstImage;
        }
    });
    
// 顯示bar


// 顯示blocks



function createBar(attraction) {}

function createBlock(attraction) {}

function renderBars(attraction) {}

function renderBlocks(startIdx, count) {}

function handleLoadMore() {}
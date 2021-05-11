const viewPointGallery = document.getElementById("viewPointGallery");
const loading = document.querySelector(".loading");
isLoading = false;

document.addEventListener("DOMContentLoaded", init)
window.addEventListener("scroll", calculateViewPointsNeeds);

function calculateViewPointsNeeds() {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    if (clientHeight + scrollTop >= scrollHeight) {
        console.log("to the bottom");

        //show the loading animation
        showLoading();
    }
}

function showLoading() {
    if (isLoading) return;

    loading.classList.add("show");
    isLoading = true;

    //load more data
    setTimeout(getMoreViewPoints, 500);
}

function init() {
    getMoreViewPoints();
}

async function getMoreViewPoints() {
    let viewPointList = await getViewPointList();
    imagePathStringsToJSON(viewPointList["data"])
    createGallery(viewPointList["data"]);
    //
    //將nextPage代入loading more，無下一頁則停止載入
    //
    if (viewPointList["nextPage"]) {
        console.log(viewPointList)
        calculateViewPointsNeeds()
    }
    console.log("oo")

}

function imagePathStringsToJSON(data) {
    return data.forEach((value, index, array) => {
        array[index]["images"] = JSON.parse(value["images"])
    })
}

async function getViewPointList(page = 1, keyword = "") {
    return new Promise((resolve, reject) => {
        let url = new URL('http://52.68.89.158:3000/api/attractions');
        url.searchParams.set('page', page);
        url.searchParams.set('keyword', keyword);

        let xhr = new XMLHttpRequest();
        xhr.open("GET", url);
        xhr.onload = function () {
            if (this.status !== 200) {
                return reject("資料讀取錯誤");
            }
            resolve(JSON.parse(this.responseText));
        };
        xhr.send();
    })
}

function createGallery(data) {
    const currentGalleryLength = viewPointGallery.children.length;
    const limit = 12;
    const startIndex = currentGalleryLength;
    const endIndex = currentGalleryLength + limit;

    let docFrag = document.createDocumentFragment();
    let partialViewPointList = data.slice(startIndex, endIndex);

    partialViewPointList.forEach((x) => {
        let card = document.createElement("div");
        card.classList.add("card");
        let cardBody = document.createElement("div");
        cardBody.classList.add("card-body");
        let cardBodyImg = document.createElement("img");
        cardBodyImg.src = x.images[0];
        cardBodyImg.alt = x.name + "圖片";
        cardBody.appendChild(cardBodyImg);
        card.appendChild(cardBody);

        let cardFooter = document.createElement("div");
        cardFooter.classList.add("card-footer");
        let cardFooterText = document.createElement("div");
        cardFooterText.classList.add("card-footer-text");
        cardFooterText.textContent = x.name;
        cardFooter.appendChild(cardFooterText);
        card.appendChild(cardFooter);
        docFrag.appendChild(card);
    });
    viewPointGallery.appendChild(docFrag);

    //hide the loading animation
    loading.classList.remove("show");
    isLoading = false;
}

function setRequest(url) {
    return new Promise((resolve, reject) => {
        let openDataAddress = url;
        let xhr = new XMLHttpRequest();
        xhr.open("GET", openDataAddress);
        xhr.onload = function () {
            if (this.status !== 200) {
                return reject("資料讀取錯誤");
            }
            resolve(JSON.parse(this.responseText));
        };
        xhr.send();
    });
}

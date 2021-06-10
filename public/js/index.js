const viewPointGallery = document.getElementById("viewPointGallery");
const loading = document.querySelector(".loading");
let isLoading = false;
let page = 1
let keyword = ""

document.addEventListener("DOMContentLoaded", init)
window.addEventListener("scroll", calculateViewPointsNeeds);
let search_btn = document.querySelector(".search_btn")
search_btn.addEventListener("click", searchKeyword)
let textInput = document.getElementById("textInput")
textInput.addEventListener("keydown", keyDownEnter)

function keyDownEnter(e) {
    if (e.keyCode === 13) searchKeyword()
}


function searchKeyword() {
    keyword = textInput.value
    page = 1
    viewPointGallery.textContent = ""
    getMoreViewPoints();
}

function calculateViewPointsNeeds() {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    if (clientHeight + scrollTop >= scrollHeight - 154) {
        showLoading();
    }
}

function showLoading() {
    if (isLoading) return;
    if (page === null) {
        loading.classList.remove("show");
        isLoading = false;
        return
    }

    loading.classList.add("show");
    isLoading = true;
    setTimeout(getMoreViewPoints, 500);
}

function init() {
    getMoreViewPoints();
}

async function getMoreViewPoints() {
    let viewPointList = await getViewPointList(page, keyword);
    page = viewPointList["nextPage"] !== undefined ? viewPointList["nextPage"]["page"] : null
    imagePathStringsToJSON(viewPointList)
    createGallery(viewPointList);
    calculateViewPointsNeeds()
}

function imagePathStringsToJSON(data) {
    if (data["error"]) return viewPointGallery.textContent = "Ops! 沒有景點，請試試其他關鍵字。"
    return data["data"].forEach((value, index, array) => {
        array[index]["images"] = JSON.parse(value["images"])
    })
}

async function getViewPointList(page, keyword) {
    return new Promise((resolve, reject) => {
        let url = new URL('http://127.0.0.1:3000/api/attractions');
        // let url = new URL('http://52.68.89.158:3000/api/attractions');
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
    if (data["error"]) return

    let docFrag = document.createDocumentFragment();

    data["data"].forEach((x) => {
        let card = document.createElement("div");
        card.classList.add("card");
        let attractionLink = document.createElement("a")
        attractionLink.href = `./attraction/${x.attraction_id}`
        card.appendChild(attractionLink)

        let cardBody = document.createElement("div");
        cardBody.classList.add("card-body");
        let cardBodyImg = document.createElement("img");
        cardBodyImg.src = x.images[0];
        cardBodyImg.alt = x.name + "圖片";
        cardBody.appendChild(cardBodyImg);
        attractionLink.appendChild(cardBody);

        let cardFooter = document.createElement("div");
        cardFooter.classList.add("card-footer");

        let cardFooterText = document.createElement("div");
        cardFooterText.classList.add("card-footer-text");
        cardFooterText.textContent = x.name;
        cardFooter.appendChild(cardFooterText);


        let cardFooterText2 = document.createElement("div");
        cardFooterText2.classList.add("card-footer-text")
        let cardFooterTextLeft = document.createElement("div")
        cardFooterTextLeft.classList.add("card-footer-left")
        cardFooterTextLeft.textContent = x.mrt
        cardFooterText2.appendChild(cardFooterTextLeft)
        let cardFooterTextRight = document.createElement("div")
        cardFooterTextRight.classList.add("card-footer-right")
        cardFooterTextRight.textContent = x.category
        cardFooterText2.appendChild(cardFooterTextRight)
        cardFooter.appendChild(cardFooterText2);


        attractionLink.appendChild(cardFooter);
        docFrag.appendChild(card);
    });
    viewPointGallery.appendChild(docFrag);

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

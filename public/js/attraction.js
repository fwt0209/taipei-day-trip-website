document.addEventListener("DOMContentLoaded", init)
let slideIndex = 1;

async function init() {
    const attraction_id = getAttractionId(window.location.pathname)
    const viewPoint = await getViewPoint(attraction_id)
    showAttractionInfo(viewPoint.data)
    createSlides(viewPoint.data.images)
    showSlides(slideIndex);
    document.addEventListener("keydown", (e) => {
        if (e.keyCode === 39) plusSlides(1)
    })
    document.addEventListener("keydown", (e) => {
        if (e.keyCode === 37) plusSlides(-1)
    })
}

function showAttractionInfo(data) {
    let name = document.getElementById("name")
    let category = document.getElementById("category")
    let mrt = document.getElementById("mrt")
    let description = document.getElementById("description")
    let address = document.getElementById("address")
    let transport = document.getElementById("transport")

    name.textContent = data.name
    category.textContent = data.category
    mrt.textContent = data.mrt
    description.textContent = data.description
    address.textContent = data.address
    transport.textContent = data.transport
}

let price = document.getElementById("price")
let morningRadioBtn = document.getElementById("morning")
morningRadioBtn.addEventListener("change", () => {
    price.textContent = "新台幣2000元"
})
let afternoonRadioBtn = document.getElementById("afternoon")
afternoonRadioBtn.addEventListener("change", () => {
    price.textContent = "新台幣2500元"
})


function createSlides(images) {
    let rawData = JSON.parse(images)
    const totalSlides = rawData.length
    let slideNumber = 0
    let slideshow = document.getElementById("slideshow")
    let docFrag = document.createDocumentFragment();
    rawData.forEach(x => {
        slideNumber++
        let slide = document.createElement("div")
        slide.classList.add("slides", "fade")
        let slideImg = document.createElement("img")
        slideImg.src = x
        slide.appendChild(slideImg)
        let slidePageText = document.createElement("div")
        slidePageText.classList.add("numbertext")
        slidePageText.textContent = `${slideNumber} / ${totalSlides}`
        slide.appendChild(slidePageText)
        docFrag.appendChild(slide)
    });

    slideNumber = 0
    let pagination = document.createElement("div")
    pagination.classList.add("pages")
    rawData.forEach(x => {
        slideNumber++
        let dot = document.createElement("span")
        dot.classList.add("dot")
        dot.addEventListener("click", () => {
            currentSlide(slideNumber)
        })
        pagination.appendChild(dot)
    });
    docFrag.appendChild(pagination)

    let prev = document.createElement("a")
    prev.classList.add("prev")
    prev.appendChild(document.createTextNode("\u276E"))
    prev.addEventListener("click", () => {
        plusSlides(-1)
    })
    docFrag.appendChild(prev)

    let next = document.createElement("a")
    next.classList.add("next")
    next.appendChild(document.createTextNode('\u276F'))
    next.addEventListener("click", () => {
        plusSlides(1)
    })
    docFrag.appendChild(next)


    slideshow.appendChild(docFrag)
}



function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("slides");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}



function getAttractionId(urlPath) {
    return urlPath.substring(urlPath.lastIndexOf("/") + 1)
}

async function getViewPoint(attraction_id) {
    return new Promise((resolve, reject) => {
        let api = new URL('http://127.0.0.1:3000/api/attraction');
        // let api = new URL('http://52.68.89.158:3000/api/attraction');
        const url = api.pathname.concat(`/${attraction_id}`)

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

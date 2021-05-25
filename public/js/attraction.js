document.addEventListener("DOMContentLoaded", init)

async function init() {
    const attraction_id = getLastUrlPath(window.location.pathname)
    const viewPoint = await getViewPoint(attraction_id)
    console.log(viewPoint)
}

let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
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

function getLastUrlPath(urlPath) {
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

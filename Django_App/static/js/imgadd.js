
const formGroup = [...document.querySelectorAll(".form-group p")];
for(let i=0;i<formGroup.length;i++){
    formGroup[i].setAttribute("id",`form-p${i}`);
}

const img = document.createElement("img");

const fileInput = document.getElementById("id_image_path");
fileInput.addEventListener('change', e => {
    img.src = window.URL.createObjectURL(e.target.files[0]);
});

const initialURL = document.getElementById("id_image_link");
if (initialURL.value) {
    img.src = initialURL.value;
} else {
    img.src = '/media/img/noimage.png'
}
initialURL.style.display = "none";

const labelImg = document.querySelector("#form-p4 label");
labelImg.after(img);

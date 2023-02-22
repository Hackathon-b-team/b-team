
const img = document.createElement("img");

const fileInput = document.getElementById("id_barcode_image");
fileInput.addEventListener('change', e => {
    img.src = window.URL.createObjectURL(e.target.files[0]);
});

img.src = '/media/img/noimage.png'

const labelImg = document.querySelector(".form-group-update label");
labelImg.after(img);

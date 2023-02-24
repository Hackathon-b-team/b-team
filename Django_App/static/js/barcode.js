
const img = document.createElement("img");
const label = document.createElement("label");

const fileInput = document.getElementById("id_barcode_image");
const imageArea = document.getElementById("image-area");

// img.src = '/media/img/noimage.png'

imageArea.appendChild(img);

label.setAttribute("id","form-group-update-label");
label.innerText = "ファイルを選択"
fileInput.before(label);
label.appendChild(fileInput);

fileInput.addEventListener('change', e => {
    img.src = window.URL.createObjectURL(e.target.files[0]);
});

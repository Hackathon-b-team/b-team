const input = document.querySelector('input[type="file"]');
const image = document.getElementById('bookimg');
input.onchange = e => {
  if (e.target.files.length) {
    const image = document.getElementById('bookimg');
    image.src = URL.createObjectURL(e.target.files[0]);
  }
};
const f = document.getElementById("myForm");
const div = document.getElementById("frame");
const evaluation = document.getElementById("evaluation");
const title = f.getElementsByTagName("p")[4];
const author = f.getElementsByTagName("p")[5];
const released = f.getElementsByTagName("p")[9];
const purchased = f.getElementsByTagName("p")[8];
const category = f.getElementsByTagName("p")[3];
const price = f.getElementsByTagName("p")[6];
const progress = f.getElementsByTagName("p")[0];
const page = f.getElementsByTagName("p")[7];
const id_evaluation = f.getElementsByTagName("p")[1];
// var inimage = f.getElementsByTagName("p")[10];
div.appendChild(title);
div.appendChild(author);
div.appendChild(released);
div.appendChild(purchased);
div.appendChild(category);
div.appendChild(price);
div.appendChild(progress);
div.appendChild(page);
evaluation.appendChild(id_evaluation);

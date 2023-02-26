const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const photo = document.getElementById('photo');
const picture = document.getElementById('picture');
const form = document.querySelector('form');

navigator.mediaDevices.getUserMedia({ video: true, audio: false })
  .then(function (stream) {
    video.srcObject = stream;
  })
  .catch(function (error) {
    console.error('mediaDevice.getUserMedia() error:', error);
    return;
  });

function takePicture() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0);
}

picture.addEventListener('click',takePicture);

form.addEventListener('submit', function (event) {
  event.preventDefault();
  photo.value = canvas.toDataURL();
  this.submit();
});

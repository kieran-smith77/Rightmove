// Get the modal
var modal = document.getElementById("myModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var modalImg = document.getElementById("modalImg");
var captionText = document.getElementById("caption");
function bigimg(img){
  modal.style.display = "block";
  modalImg.dataset.id = img.dataset.id
  modalImg.src = img.src;
  captionText.innerHTML = img.alt;
  document.addEventListener("keydown", keyDownTextField, false);
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

if (span) {
span.onclick = function() {
  modal.style.display = "none";
  document.removeEventListener("keydown", keyDownTextField, false);
}}

function keyDownTextField(e) {
  var keyCode = e.keyCode;
  if(keyCode==37 || keyCode==38) {
    var currentid = modalImg.dataset.id
    var new_img = document.getElementById('img'+(parseInt(currentid)-1))
    if (!new_img) {
      new_img = document.getElementById('img1')
    }
    bigimg(new_img)
  } else if (keyCode==39 || keyCode==40) {
    var currentid = modalImg.dataset.id
    var new_img = document.getElementById('img'+(parseInt(currentid)+1))
    if (!new_img) {
      new_img = document.getElementById('img1')
    }
    bigimg(new_img)
  } else if (keyCode==27) {
    modal.style.display = "none";
    document.removeEventListener("keydown", keyDownTextField, false);
  } else {
    alert(keyCode);
  }
}

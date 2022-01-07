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

// Initialize and add the map
function initMap() {
  const mapobj = document.getElementById("map");

  const house = {
    lat: parseFloat(mapobj.dataset.latitude),
    lng: parseFloat(mapobj.dataset.longitude)
  };
  // The map, centered at Uluru
  const map = new google.maps.Map(mapobj, {
    zoom: 15,
    center: house,
    styles: [
    {
      "featureType": "poi",
      "stylers": [
        { "visibility": "off" }
      ]
    }
  ]
  });
  // The marker, positioned at Uluru
  const marker = new google.maps.Marker({
    position: house,
    map: map,
  });
}

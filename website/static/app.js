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
  document.addEventListener('click', outsideClickListener);  
}

function outsideClickListener(element){
  if (element.srcElement.id == 'myModal') {
    changeImage('esc')
  }   
}
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

if (span) {
span.onclick = function() {
  modal.style.display = "none";
  document.removeEventListener("keydown", keyDownTextField, false);
}}


let touchstartX = 0
let touchendX = 0

function checkDirection() {
  if (modal && modal.style.display == "block" && Math.abs(touchstartX - touchendX) > 300) {
    if (touchendX < touchstartX) {
      changeImage('next')
    } else {
      changeImage('previous')
    }
  } else if ( Math.abs(touchstartX - touchendX) > 300) {
    if (touchendX > touchstartX) {
      if (window.location.pathname == '/bad-ones') {
        window.location.href = '/'
      } else if (window.location.pathname == '/'){
        window.location.href = "/good-ones";
      }
    } else {
      if (window.location.pathname == '/good-ones') {
        window.location.href = '/'
      } else if (window.location.pathname == '/') {
        window.location.href = "/bad-ones";
      }
    }
  } 
}

document.addEventListener('touchstart', e => {
  touchstartX = e.changedTouches[0].screenX
})

document.addEventListener('touchend', e => {
  touchendX = e.changedTouches[0].screenX
  checkDirection()
})

function keyDownTextField(e) {
  var keyCode = e.keyCode;
  if (keyCode==37 || keyCode==38) {
    changeImage('previous')
  } else if (keyCode==39 || keyCode==40) {
    changeImage('next')
  } else if (keyCode==27) {
    changeImage('esc')
  }
}

function changeImage(direction) {
  if(direction == 'previous') {
    var currentid = modalImg.dataset.id
    var new_img = document.getElementById('img'+(parseInt(currentid)-1))
    if (!new_img) {
      new_img = document.getElementById('img1')
    }
    bigimg(new_img)
  } else if (direction == 'next') {
    var currentid = modalImg.dataset.id
    var new_img = document.getElementById('img'+(parseInt(currentid)+1))
    if (!new_img) {
      new_img = document.getElementById('img1')
    }
    bigimg(new_img)
  } else if (direction == 'esc') {
    modal.style.display = "none";
    document.removeEventListener("keydown", keyDownTextField, false);
    document.removeEventListener('click', outsideClickListener);
  } else {
    alert(direction, 'unknown');
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

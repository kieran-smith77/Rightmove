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
  
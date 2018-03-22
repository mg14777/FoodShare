function buildNeighbourhoodMap(userlocation) {
  console.log(userlocation);
  
  var xhr = new XMLHttpRequest();
  xhr.open('GET',"/localitysearch?lat="+userlocation.coords.latitude+"&lng="+userlocation.coords.longitude,true);
  xhr.send();
  xhr.addEventListener("readystatechange", localitySearchResponse, false);  
  function localitySearchResponse() {
    if(xhr.readyState == "4") {
        console.log('Request Complete');
        nearby_contributions_coords = JSON.parse(xhr.responseText);
        console.log(nearby_contributions_coords);
        console.log(nearby_contributions_coords[0]);
        console.log(nearby_contributions_coords[0]["lat"]);
        initNeighbourhoodMap(userlocation,nearby_contributions_coords);
    }
    else {
        console.log('False alarm');
        console.log(xhr.responseText);
    }

  }  
}
function initNeighbourhoodMap(userlocation,nearby_contributions_coords) {
  var userPos = {lat: userlocation.coords.latitude, lng: userlocation.coords.longitude};
  var map = new google.maps.Map(document.getElementById('nearby-food-map'), {
    center: userPos,
    zoom: 15
  });
  for(var i=0; i < nearby_contributions_coords.length; i++) {
    var marker = new google.maps.Marker({
        position: nearby_contributions_coords[i],
        map: map
      });
    var user_marker = new google.maps.Marker({
        position: userPos,
        map: map,
        label: "You"
      });
  }

}
function showError(error) {
    var x = document.getElementById('nearby-food-map');
    switch(error.code) {
        case error.PERMISSION_DENIED:
            x.innerHTML = "User denied the request for Geolocation."
            break;
        case error.POSITION_UNAVAILABLE:
            x.innerHTML = "Location information is unavailable."
            break;
        case error.TIMEOUT:
            x.innerHTML = "The request to get user location timed out."
            break;
        case error.UNKNOWN_ERROR:
            x.innerHTML = "An unknown error occurred."
            break;
    }
}
( function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(buildNeighbourhoodMap, showError);
    }
}
)();
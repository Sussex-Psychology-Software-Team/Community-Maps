const userData = {lat:0,lng:0}

// Create map
const map = L.map('map',{
        //zoomSnap: 0.5
    })
    .setView([30, 0], 3);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const popup = L.popup();

function onMapClick(e) {
    overpassTurboQuery(e.latlng)
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
    const marker = L.marker(e.latlng).addTo(map);
    saveClick(e.latlng)
}

function saveClick(latlng){
    userData.lat = latlng.lat
    userData.lng = latlng.lng
    console.log(userData)
}
map.on('click', onMapClick);

function overpassTurboQuery(latLng){
    const query = `
        [out:json];
        (
        is_in(${latLng.lat},${latLng.lng})->.a;
        area.a[admin_level][boundary=administrative];
        );
        out body;
        >;
        out skel qt;
    `
    // Encode the query for the URL
    const url = "https://overpass-api.de/api/interpreter?data=" + encodeURIComponent(query);
    // Fetch the JSON data from the Overpass API
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log("Administrative boundaries data:", data);
        for(let d=0; d<data.elements.length; d++){
            const tags = data.elements[d].tags
            console.log(tags.int_name ? tags.int_name : 'name:en' in tags ? tags['name:en'] : tags.name)
        }
    })
    .catch(error => {
        console.error("Error fetching administrative boundaries:", error);
    });
}


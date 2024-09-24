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
    //getLocationDetails(e.latlng)
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

async function getLocationDetails(latLng){
    url = 'api.geonames.org/countrySubdivisionJSON?lat='+latLng.lat+'&lng='+latLng.lng+'&maxRows=10&radius=40&username=demo'
    // Make the fetch request with the provided options
    fetch(url)
    .then(response => {
        // Check if the request was successful
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        // Parse the response as JSON
        return response.json();
    })
    .then(data => {
        // Handle the JSON data
        console.log(data);
    })
    .catch(error => {
        // Handle any errors that occurred during the fetch
        console.error('Fetch error:', error);
    });
}



// BOUNDARIES **************************************************
// Add interactivity to country layer
function onEachBoundary(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

// Event handlers for highlighting countries
function highlightFeature(e) {
    const layer = e.target
    console.log(layer.feature.properties)
    layer.setStyle({
        weight: 2,
        color: 'blue',
        fillOpacity: 0.2
    })
    .bringToFront()
    .bindPopup(layer.feature.properties.ADMIN);
}

function resetHighlight(e) {
    console.log(e)
    countryLayer.resetStyle(e.target);
}

// Zoom to a feature on click
function zoomToFeature(e) {
    console.log(e.target.feature.properties)
    map.fitBounds(e.target.getBounds());
    // Example usage: Fetch boundaries for "Germany" with a maximum admin level of 8
    fetchAdminBoundaries(e.target.feature.properties.ISO_A2);
}

function fetchAdminBoundaries(iso) {
    // Construct the Overpass API query
    const query = `
        [out:json];
        relation["ISO3166-2"~"^${iso}"]
        ["admin_level"="6"]
        ["type"="boundary"]
        ["boundary"="administrative"];
        out body;
        >;
        out skel qt;
    `;

    // Encode the query for the URL
    const url = "https://overpass-api.de/api/interpreter?data=" + encodeURIComponent(query);

    // Fetch the JSON data from the Overpass API
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log("Administrative boundaries data:", data);
        // Convert the Overpass JSON to GeoJSON using osmtogeojson
        const geojson = osmtogeojson(data);
        // Plot the GeoJSON on the Leaflet map
        const newLayer = L.geoJson(geojson, layerParams)
        newLayer.addTo(map);
        // Fit the map bounds to the GeoJSON layer
        map.fitBounds(L.geoJson(geojson).getBounds());
    })
    .catch(error => {
        console.error("Error fetching administrative boundaries:", error);
    });
}

// Load GeoJSON data for countries
const layerParams = {
    style: {
        fillColor: 'blue',
        weight: 1,
        opacity: 1,
        color: 'black',
        fillOpacity: 0
    },
    onEachFeature: onEachBoundary
}

const countryLayer = L.geoJson.ajax("https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson", layerParams);

// Add country layer by default (initial zoom level)
countryLayer.addTo(map);

// // Switch layers based on zoom level
// map.on('zoomend', function () {
//     var currentZoom = map.getZoom();

//     // Set a threshold zoom level (e.g., 6)
//     if (currentZoom >= 6) {
//         // Remove country layer and add city layer
//         if (map.hasLayer(countryLayer)) {
//             map.removeLayer(countryLayer);
//         }
//         if (!map.hasLayer(cityLayer)) {
//             map.addLayer(cityLayer);
//         }
//     } else {
//         // Remove city layer and add country layer
//         if (map.hasLayer(cityLayer)) {
//             map.removeLayer(cityLayer);
//         }
//         if (!map.hasLayer(countryLayer)) {
//             map.addLayer(countryLayer);
//         }
//     }
// });


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

// Boundaries
var boundariesLayer = null; // Placeholder for the dynamically fetched boundaries layer
let currentAdminLevel = 1

// Function to build Overpass API query based on map bounds and zoom level
function buildOverpassQuery(bounds, zoom) {
    var bbox = `${bounds.getSouth()},${bounds.getWest()},${bounds.getNorth()},${bounds.getEast()}`;

    // Admin levels: 2 = country, 4 = state/province
    let adminLevels;
    if (zoom <= 5) {
        adminLevels = 2; // Country boundaries for low zoom levels
    } else if (zoom <= 10) {
        adminLevels = 4; // State boundaries for medium zoom levels
    } else {
        adminLevels = 6; // For higher zoom levels, still use state boundaries to reduce data
    }

    if(currentAdminLevel === adminLevels) return false
    currentAdminLevel = adminLevels
    // Overpass query to fetch administrative boundaries within the bounding box
    return `[out:json][timeout:180];
            (
              relation["boundary"="administrative"]["admin_level"~"${adminLevels}"](${bbox});
            );
            out body;
            >;
            out skel qt;`;
}

// Fetch administrative boundaries from Overpass API
function fetchBoundaries() {
    var bounds = map.getBounds();
    var zoom = map.getZoom();
    var overpassQuery = buildOverpassQuery(bounds, zoom);
    if(!overpassQuery) return
    console.log(overpassQuery)
    var overpassURL = "https://overpass-api.de/api/interpreter?data=" + encodeURIComponent(overpassQuery);

    fetch(overpassURL)
        .then(response => response.json())
        .then(data => {
            if (boundariesLayer) {
                map.removeLayer(boundariesLayer); // Remove the previous boundaries layer
            }

            var geojson = osmtogeojson(data);
            boundariesLayer = L.geoJson(geojson, {
                style: function (feature) {
                    return {
                        color: 'blue',
                        weight: 2,
                        fillOpacity: 0.2
                    };
                },
                onEachFeature: function (feature, layer) {
                    // Add mouseover and mouseout events for highlighting
                    layer.on({
                        mouseover: function (e) {
                            var layer = e.target;
                            layer.setStyle({
                                weight: 3,
                                color: 'red',
                                fillOpacity: 0.4
                            });
                            layer.bringToFront();
                        },
                        mouseout: function (e) {
                            boundariesLayer.resetStyle(e.target); // Reset style on mouseout
                        },
                        click: function (e) {
                            map.fitBounds(e.target.getBounds()); // Zoom to the clicked feature
                        }
                    });
                }
            });

            boundariesLayer.addTo(map);
        })
        .catch(error => console.error("Error fetching boundaries:", error));
}

// Fetch boundaries when the map is zoomed or moved
map.on('zoomend', fetchBoundaries);
map.on('moveend', fetchBoundaries);

// Fetch boundaries when the map first loads
fetchBoundaries();
const HERE_API_KEY = 'Oss3WjIK8mBoyFOIwwF64d-aK8F_f8xCl2zjXQ7YRVs'

const platform = new H.service.Platform({
    apikey: HERE_API_KEY
});

const defaultLayers = platform.createDefaultLayers();

const map = new H.Map(document.getElementById('mapContainer'),
    defaultLayers.vector.normal.map,
    {
        // map auto centers on Michigan unless a user chooses to input their location
        center: { lat: lat, lng: lng },
        zoom: 20,
        pixelRatio: window.devicePixelRatio || 1
    }
);

// This adds a resize listener to make sure that the map occupies the whole container
window.addEventListener('resize', () => map.getViewPort().resize());
//Step 3: make the map interactive
// MapEvents enables the event system
// Behavior implements default interactions for pan/zoom (also on mobile touch environments)
const behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

// Add marker for the pin
let LocationOfMarker = { lat: lat, lng: lng };
// Create a marker icon from an image URL:
const icon = new H.map.Icon('/static/leafpls.PNG');

// Create a marker using the previously instantiated icon:
let marker = new H.map.Marker(LocationOfMarker, { icon: icon });

// Add the marker to the map:
map.addObject(marker);
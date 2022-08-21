const HERE_API_KEY = 'Oss3WjIK8mBoyFOIwwF64d-aK8F_f8xCl2zjXQ7YRVs'

// on an input location click load a map showing the address typed in
const submit_location_form = document.querySelector('.submit_form')

submit_location_form.addEventListener('submit', async function handleLocationForm(e) {
    e.preventDefault()
    // clear the map container so only one map shows up at a time
    const map_container = document.querySelector('#mapContainer')
    map_container.innerHTML = ''

    const location = document.querySelector('.location_input')
    const HERE_url = 'https://geocode.search.hereapi.com/v1/geocode'
    let resp = await axios.get(HERE_url, {
        params: {
            apikey: HERE_API_KEY,
            q: location.value
        }
    })
    if (resp.data.items.length == 0) {
        alert(`${location.value} is not a valid address`)
    }

    const platform = new H.service.Platform({
        apikey: HERE_API_KEY
    });
    const defaultLayers = platform.createDefaultLayers();

    const map = new H.Map(document.getElementById('mapContainer'),
        defaultLayers.vector.normal.map,
        {
            // map auto centers on Michigan unless a user chooses to input their location
            center: { lat: resp.data.items[0].position.lat, lng: resp.data.items[0].position.lng },
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

    // Add event listener for a tap, on a tap create a bubble with a form in it so a user can add a plant.
    map.addEventListener('tap', function addBubble(evt) {
        // Log 'tap' and 'mouse' events:
        // console.log(evt.type, evt.currentPointer.type, evt.target.f.Y.lat, evt.target.f.Y.lng);
        if (evt.target.data) {
            let bubble = new H.ui.InfoBubble({ lng: evt.target.a.lng, lat: evt.target.a.lat }, {
                content: evt.target.data
            });
            // Add info bubble to the UI:
            ui.addBubble(bubble);

        } else {
            let latitude = evt.target.f.Y.lat
            let longitude = evt.target.f.Y.lng


            let button = document.createElement("button")
            const input = document.createElement("input")
            const div = document.createElement("div")
            input.setAttribute("type", "text")
            button.setAttribute("class", "submit")
            button.innerText = "Submit"
            div.appendChild(input)
            div.append(button)


            let bubble = new H.ui.InfoBubble({ lng: evt.target.f.Y.lng, lat: evt.target.f.Y.lat }, {
                content: div
            });

            // Add info bubble to the UI:
            ui.addBubble(bubble);

            button.addEventListener('click', function addPlant(e) {
                e.preventDefault()
                const plant = input.value
                const dict_values = { plant, latitude, longitude }
                const s = JSON.stringify(dict_values);
                // console.log(s);
                // send the form info to python so it can be added to the database
                $.ajax({
                    url: "handle_map",
                    type: "POST",
                    dataType: 'json',
                    contentType: "application/json",
                    data: s,
                    success: function (result) {
                        let LocationOfMarker = { lat: result.latitude, lng: result.longitude };
                        // Create a marker icon from an image URL:
                        const icon = new H.map.Icon('/static/leafpls.PNG');

                        // Create a marker using the previously instantiated icon:
                        let marker = new H.map.Marker(LocationOfMarker, { icon: icon }, { data: plant });

                        // Add the marker to the map:
                        map.addObject(marker);
                    }

                });
                if (evt.target.data) {
                    let bubble = new H.ui.InfoBubble({ lng: evt.target.a.lng, lat: evt.target.a.lat }, {
                        content: evt.target.data
                    });
                    // Add info bubble to the UI:
                    ui.addBubble(bubble);
                }
            })

        };
    })

    // load all the pins
    const base_url = 'http://127.0.0.1:5000/api'
    const pin_resp = await axios.get(`${base_url}/pins`)

    for (let data of pin_resp.data) {
        let LocationOfMarker = { lat: data.latitude, lng: data.longitude };
        // Create a marker icon from an image URLn:
        const icon = new H.map.Icon('/static/leafpls.PNG');
        // Create a marker using the previously instantiated icon:
        let marker = new H.map.Marker(LocationOfMarker, { icon: icon, data: data.plant });

        // Add the marker to the map:
        map.addObject(marker);
    }



    // Create the default UI components
    const ui = H.ui.UI.createDefault(map, defaultLayers);
    // show the user the address so they can relocate it if needed
    map_container.prepend(`Showing map for ${resp.data.items[0].address.label}`)
}
)








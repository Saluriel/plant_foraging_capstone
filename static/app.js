const HERE_API_KEY = 'Oss3WjIK8mBoyFOIwwF64d-aK8F_f8xCl2zjXQ7YRVs'
const HERE_url = 'https://geocode.search.hereapi.com/v1/geocode'

const submit_location_form = document.querySelector('.submit_form')
const map_container = document.querySelector('#mapContainer')



class Map {
    constructor(location) {
        this.location = location
        this.map_data = {}
    }

    async createMap() {
        this.map_data = await axios.get(HERE_url, {
            params: {
                apikey: HERE_API_KEY,
                q: this.location
            }
        })

        let resp_length = this.map_data.data.items.length
        if (resp_length == 0) {
            alert(`${location} is not a valid address`)
        }

        const platform = new H.service.Platform({
            apikey: HERE_API_KEY
        });
        
        const defaultLayers = platform.createDefaultLayers();
    }
}

async function putMapOnPage(e) {
    e.preventDefault()
    const location = document.querySelector('.location_input')
    const m = new Map(location.value)
    
    await m.createMap()
    console.log(m)
    console.log(m.location)
    console.log(m.map_data)

}

submit_location_form.addEventListener('submit', putMapOnPage)
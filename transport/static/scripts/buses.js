var map = L.map('map').setView([43.3445, -8.425], 13);

var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>',
    minZoom: 13
}).addTo(map);

function icono(feature, latlng) {
    let iconoBus = L.icon({
        iconUrl: '/static/icono-bus-32.png',

        iconSize: [32, 32],
        iconAncho: [16, 16],
        popupAnchor: [16, 28],
    })
    return L.marker(latlng, { icon: iconoBus })
}

let opts = {
    pointToLayer: icono
}

L.geoJson(buses, opts).addTo(map);

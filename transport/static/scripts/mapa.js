// Muestra un mapa con todas las paradas utilizando Leaflet-js
document.getElementById('map').innerHTML = '';

// var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
var tiles = L.tileLayer('https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://osm.ogr/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',
    minZoom: 13
});

var bright = L.tileLayer('https://d.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://osm.ogr/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',
    minZoom: 13
});

var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://osm.ogr/copyright">OpenStreetMap</a>',
    minZoom: 13
});

var pnoa = L.tileLayer('https://tms-pnoa-ma.idee.es/1.0.0/pnoa-ma/{z}/{x}/{-y}.jpeg', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://pnoa.ign.es">PNOA</a>, <a href="https://idee.es">IDEE</a>',
    minZoom: 13
});


if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    var map = L.map('map', {
        center: [43.3445, -8.425],
        zoom: 13,
        layers: [tiles]
    });
}
else {
    var map = L.map('map', {
        center: [43.3445, -8.425],
        zoom: 13,
        layers: [bright]
    });
}

var oscuro = {
    'Osm': osm,
    'Claro': bright,
    'Oscuro': tiles,
    'PNOA (ortofotos)': pnoa
};

var layerControl = L.control.layers(oscuro).addTo(map);

// const layerControl = L.control.layers(baseLayers).addTo(map);

function onEachFeature(feature, layer) {
    if(feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}

var geojson = L.geoJson(paradas, { onEachFeature: onEachFeature});
var paradas = L.markerClusterGroup({
    spiderflyOnMaxZoom: false,
    showCoverageOnHover: false,
    zoomToBoundsOnClick: true,
});

paradas.addLayer(geojson);
map.addLayer(paradas);

var userIcon = L.icon({
    iconUrl: 'static/icons/userIcon.png',

    iconSize: [48, 48],
    iconAnchor: [24, 48]
});

var marcador = L.icon({
    iconUrl: 'static/icons/marcador-3.png',

    iconSize: [32, 32],
    iconAnchor: [16, 16]
});

map.locate({setView: true, maxZoom: 16});

function onLocationFound(e) {
    // L.marker(e.latlng, {icon: userIcon}).addTo(map)
    L.marker(e.latlng, {icon: marcador}).addTo(map)
}
map.on('locationfound', onLocationFound);
// map.setMaxBounds(map.getBounds());
var topleft = L.latLng(43.3925, -8.4585),
    bottomright = L.latLng(43.2945, -8.3755);
map.setMaxBounds(L.latLngBounds(topleft, bottomright));
// L.rectangle([[43.3925, -8.4525], [43.2945, -8.3865]], {color: "#ff7800", weight: 1}).addTo(map);
//L.rectangle([[43.3925, -8.4585], [43.2945, -8.3755]], {color: "#ff7800", weight: 1}).addTo(map);

/*function onLocationError(e) {
    alert(e.message);
}
map.on('locationerror', onLocationError);*/

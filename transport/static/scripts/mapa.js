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
    'Oscuro': tiles
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

map.locate({setView: true, maxZoom: 16});

function onLocationFound(e) {
    L.marker(e.latlng, {icon: userIcon}).addTo(map)
}
map.on('locationfound', onLocationFound);

/*function onLocationError(e) {
    alert(e.message);
}
map.on('locationerror', onLocationError);*/

provider = new URLSearchParams(window.location.search).get('mapa');
if(provider == 'osm') {
    tiles = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
}
else if(provider == 'carto-light') {
    tiles = 'https://c.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png';
}
else if(provider == 'carto-dark') {
    tiles = 'https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png';
}
else if(provider == 'pnoa') {
    tiles = 'https://tms-pnoa-ma.idee.es/1.0.0/pnoa-ma/{z}/{x}/{-y}.jpeg';
}
else {
    if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        tiles = 'https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png';
    }
    else {
        tiles = 'https://c.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png';
        // tiles = 'https://c.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png';
    }
}

// var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
document.getElementById('mapa-linea').innerHTML = '';

// Mapa de parada
var map = L.map('mapa-linea', {
    /* center: ubicacion, */
    center: [43.3445, -8.425],
    zoom: 12,
    // dragging: false,
    draggin: true,
    // boxZoom: false,
    boxZoom: true,
    scrollWheelZoom: 'center',
    // zoomControl: false,
    zoomControl: true,
    doubleClickZoom: 'center',
    zoomDelta: 0.5,
});

var tiles = L.tileLayer(tiles, {
    maxZoom: 19,
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>, &copy; <a href="https://pnoa.ign.es">PNOA</a>',
    minZoom: 2
}).addTo(map);

function onEachFeature(feature, layer) {
    if(feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}

var stopIcon = L.icon({
    iconUrl: '/static/icons/maps/punto.png',

    iconSize: [16, 16],
    iconAnchor: [8, 8]
});

L.Marker.prototype.options.icon = stopIcon;

var geojson = L.geoJson(paradas, { onEachFeature: onEachFeature });

map.addLayer(geojson);
map.fitBounds(geojson.getBounds());

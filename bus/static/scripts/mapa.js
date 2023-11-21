// Muestra un mapa con todas las paradas utilizando Leaflet-js
document.getElementById('map').innerHTML = '';

idioma = new URLSearchParams(window.location.search).get('lang');   // Guardar el idioma
estilo = new URLSearchParams(window.location.search).get('mapa');   // Guardar el estilo del mapa


// Establecer el estilo del mapa en función del de la página o del parámetro
if(estilo == 'osm') { style = [osm] }
else if(estilo == 'pnoa') { style = [pnoa] }
else if(estilo == 'carto-light') { style = [bright] }
else if(estilo == 'carto-dark' || window.matchMedia('(prefers-color-scheme: dark)').matches) { style = [dark] }
else { style = [bright] }

var mapa = L.map('map', {
    center: [43.3445, -8.425],
    zoom: 13,
    layers: style
});

// Lista de estilos
var estilos = {
    'Osm': osm,
    'Claro': bright,
    'Oscuro': dark,
    'PNOA (ortofotos)': pnoa,
};

var layerControl = L.control.layers(estilos).addTo(mapa);   // Añadir el selector de estilos

function onEachFeature(feature, layer) {
    if(feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}

// Añadir los marcadores al mapa
var geojson = L.geoJson(paradas, { onEachFeature: onEachFeature});
var paradas = L.markerClusterGroup({
    spiderflyOnMaxZoom: false,
    showCoverageOnHover: false,
    zoomToBoundsOnClick: true,
});

paradas.addLayer(geojson);
mapa.addLayer(paradas);

// Marcador para la posición del usuario
var marcador = L.icon({
    iconUrl: 'static/icons/marcador-4.png',

    iconSize: [32, 32],
    iconAnchor: [16, 16]
});

// mapa.locate({setView: true, maxZoom: 16, watch: true});

// Centrar la vista en la posición del usuario
var usuario = L.circleMarker([0, 0], {radius: 8, color: '#b39ddb', fillColor: '#673ab7', fillOpacity: 1, weight: 2}).addTo(mapa);
var precision = L.circle([0, 0], 0, {color: '#673ab7', fillColor: '#673ab7', fillOpacity: 0.15, weight: 2, interactive: false}).addTo(mapa);
var centro;

function onLocationFound(e) {
    console.log('actualizar');
    usuario.setLatLng(e.latlng);
    precision.setLatLng(e.latlng);
    precision.setRadius(e.accuracy/2);
    if(centro == undefined || centro == e.latlng) {
        mapa.setView(e.latlng, 16);
    }
    centro = e.latlng;
    console.log('fin de actualizar');
}

mapa.on('locationfound ', onLocationFound);
mapa.locate({setView: false, watch: true});

var topleft = L.latLng(43.3925, -8.4585),
    bottomright = L.latLng(43.2945, -8.3755);
// L.rectangle(L.latLngBounds(topleft, bottomright), {color: '#FF9800', fillColor: '#FF9800', weight: 2, fillOpacity: 0.25}).addTo(mapa);  // Límites del mapa
mapa.setMaxBounds(L.latLngBounds(topleft, bottomright));

/* mapa.on('locationerror', flash_error('Error al buscar tu ubicación'));   */

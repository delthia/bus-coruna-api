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
    iconUrl: 'static/icons/marcador-3.png',

    iconSize: [32, 32],
    iconAnchor: [16, 16]
});

mapa.locate({setView: true, maxZoom: 16});

// Centrar la vista en la posición del usuario
function onLocationFound(e) { L.marker(e.latlng, {icon: marcador}).addTo(mapa) };
mapa.on('locationfound', onLocationFound);

var topleft = L.latLng(43.3925, -8.4585),
    bottomright = L.latLng(43.2945, -8.3755);
mapa.setMaxBounds(L.latLngBounds(topleft, bottomright));

mapa.on('locationerror', flash_error('Error al buscar tu ubicación'));

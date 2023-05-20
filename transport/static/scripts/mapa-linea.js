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
    zoomDelta: 1,
    zoomSnap: 0.2,
});

var tiles = L.tileLayer(tiles, {
    maxZoom: 19,
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>',
    minZoom: 2
}).addTo(map);

function onEachFeature(feature, layer) {
    if(feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}

var stopIcon = L.icon({
    iconUrl: '/static/icons/maps/punto.png',

    iconSize: [8, 8],
    iconAnchor: [4, 4]
});

L.Marker.prototype.options.icon = stopIcon;

var estiloLineas = {
    "color": "#5e31b1",
    "weight": 2,
    "opacity": 1
};

var geojson = L.geoJson(paradas, { onEachFeature: onEachFeature });
var lin = L.geoJson(linea, { onEachFeature: onEachFeature, style: estiloLineas });

map.addLayer(geojson);
map.addLayer(lin);
map.fitBounds(geojson.getBounds());

var topleft = L.latLng(43.3925, -8.4585),
    bottomright = L.latLng(43.2945, -8.3755);
// map.setMaxBounds(L.latLngBounds(topleft, bottomright));

// Tabla de salidas
fetch('/api/linea/'+window.location.pathname.split('/')[window.location.pathname.split('/').length-1]+'/salidas/20230520', {
    method: 'GET'
})
.then(function(response) { return response.json(); })
.then(function(json) {
    const obj = json;
    ancho = 5
    // ida
    a = 0
    tabla = ''
    while(a < obj.ida.length/ancho){
        // document.getElementById('horario-linea-ida').innerHTML += '<tr>'
        fila = ''
        for(i=0;i<5;i++){
            if(obj.ida[i+a*ancho] != undefined) { fila += '<td>'+obj.ida[i+a*ancho]+'</td>' }
            else { break; }
        }
        a += 1
        tabla += '<tr>'+fila+'</tr>'
    }
    document.getElementById('horario-linea-ida').innerHTML += tabla
    // vuelta
    a = 0
    tabla = ''
    while(a < obj.vuelta.length/ancho){
        // document.getElementById('horario-linea-ida').innerHTML += '<tr>'
        fila = ''
        for(i=0;i<5;i++){
            if(obj.vuelta[i+a*ancho] != undefined) { fila += '<td>'+obj.vuelta[i+a*ancho]+'</td>' }
            else { break; }
        }
        a += 1
        tabla += '<tr>'+fila+'</tr>'
    }
    document.getElementById('horario-linea-vuelta').innerHTML += tabla
})
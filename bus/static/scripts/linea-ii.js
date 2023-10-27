// Actualiza el diagrama de líneas, el calendario, y genera el mapa

// Preparar la página para el funcionamiento del script
idioma = new URLSearchParams(window.location.search).get('lang');   // Guardar el idioma

// Configuración del mapa

// Mostrar los elementos necesarios
document.getElementById('msg-js').style.display = "none";   // Ocultar el error
document.getElementById('salidas').style.display = "";  // Enseñar el botón de salidas
document.getElementById('boton-recarga').style.display = "";    // Enseñar el botón de recarga
document.getElementById('mapa-linea').innerHTML = "";   // Enseñar el mapa de línea
document.getElementById('leyenda').style.display = "";  // Mostrar la leyenda de la página

// Programar la ejecución de la función de actualización de la página
if(document.getElementById('estado') == null) {
    actualizar(0);  // Actualizar al cargar la página
    setInterval(function() { actualizar(last) }, 30000);   // Actualizar los datos cada 30s
}
else {
    // Ocultar el botón de actualización cuando la línea está inactiva
    document.getElementById('boton-recarga').style.display = 'none';
}


function actualizar(last) {
    var now = new Date();

    if(now-last >= 1) {
        window.last = now;
        id_linea = window.location.pathname.substring(window.location.pathname.lastIndexOf('/')+1)

        actualizar_diagrama(id_linea);
        actualizar_mapa(id_linea);

        document.getElementById('t').innerHTML = cadenas[idioma][3]+': '+now.toLocaleString(cadenas[idioma][4]);
    }
    else {
        flash_error(cadenas[idioma][2]);
    }
}

// Crear el mapa
estilo = new URLSearchParams(window.location.search).get('mapa');   // Guardar el estilo de mapa

if(estilo == 'osm') { style = [osm] }
else if(estilo == 'pnoa') { style = [pnoa] }
else if(estilo == 'carto-light') { style = [bright] }
else if(estilo == 'carto-dark' || window.matchMedia('(prefers-color-scheme: dark)').matches) { style = [dark] }
else { style = [bright] }

// Configuración del mapa
var mapa = L.map('mapa-linea', {
    center: [43.3445, -8.425],
    zoom: 12,
    scrollWhellZoom: 'center',
    doubleClickZoom: 'center',
    zoomSnap: 0.2,
    layers: style,
})

function onEachFeature(feature, layer) { if(feature.properties && feature.properties.popupContent) { layer.bindPopup(feature.properties.popupContent); } }

// estilos del mapa
var iconoParada = L.icon({
    iconUrl: '/static/icons/maps/punto.png',

    iconSize: [8, 8],
    iconAnchor: [4, 4],
});
L.Marker.prototype.options.icon = iconoParada;

var iconoBus = L.icon({
    iconUrl: '/static/icons/icono-bus-32.png',

    iconSize: [16, 16],
    iconAnchor: [8, 8],
});

var estiloLinea = {
    "color": "#5e31b1",
    "weight": 2,
    "opacity": 1,
}

// Añadir los datos al mapa
mapa.addLayer(L.geoJson(paradas, {onEachFeature: onEachFeature}));
mapa.addLayer(L.geoJson(linea, {onEachFeature: onEachFeature, style: estiloLinea}));
mapa.fitBounds(L.geoJson(paradas).getBounds());
L.Marker.prototype.options.icon = iconoBus;

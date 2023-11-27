// Actualiza el diagrama de líneas, el calendario, y genera el mapa

idioma = new URLSearchParams(window.location.search).get('lang');   // Guardar el idioma
estilo = new URLSearchParams(window.location.search).get('mapa');   // Guardar el estilo de mapa
document.getElementById('msg-js').style.display = "none";   // Ocultar el error
document.getElementById('salidas').style.display = "";
document.getElementById('boton-recarga').style.display = "";
document.getElementById('mapa-linea').innerHTML = "";
document.getElementById('leyenda').style.display = "";
if(document.getElementById('estado') == null) {
    actualizar(0);  // Actualizar al cargar la página
    setInterval(function() { actualizar(last) }, 30000);   // Actualizar los datos cada 30s
}
else {
    document.getElementById('boton-recarga').style.display = 'none';
}

// Diagrama
var last = new Date();  // Momento en el que se actualizaron los datos por última vez

function actualizar(last) {
    var now = new Date();

    if(now-last >= 15000) {
        window.last = now;

        // Descargar los datos y actualizar la información
        url = '/api/linea/'+window.location.pathname.substring(window.location.pathname.lastIndexOf('/')+1)+'/buses';
        fetch(url, {
            method: 'GET'
        })
        .then(function(response) { return response.json(); })
        .then(function(json) {
            const obj = json['paradas'];    // Almacenar los datos en una variable

            // Actualizar los iconos
            buses(obj[0], 'ida');
            buses(obj[1], 'vuelta');

            function buses(datos, c) {
                datos = datos['paradas'];
                document.getElementById('buses-'+c).innerHTML = '';

                if(datos != undefined) { // Si existen los datos
                    for(i=0; i<datos.length; i++) {
                        const x = datos[i]['buses'][0]['distancia']*(document.getElementById(c).offsetHeight-70)+8; // Posición del icono
                        // Clases para los estilos del icono
                        if(datos[i]['buses'][0]['estado'] == 0) {
                            clase = ' simbolo_bus_parada ';
                        }
                        else if(datos[i]['buses'][0]['estado'] == 1) {
                            clase = ' ';
                        }
                        else {
                            clase = ' simbolo_bus-otro ';
                        }
                        document.getElementById('buses-'+c).innerHTML += '<div style="margin-top: '+x+'px; position: absolute"><span class="material-symbols-outlined simbolo_bus'+clase+'">directions_bus</span></div>';
                    }
                }
                document.getElementById('t').innerHTML = cadenas[idioma][3]+': '+now.toLocaleString(cadenas[idioma][4]);
            }
        })
    }
    else { flash_error(cadenas[idioma][2]); }
}

// Mapa
// Establecer el estilo del mapa en función del de la página o del parámetro
if(estilo == 'osm') { style = [osm] }
else if(estilo == 'pnoa') { style = [pnoa] }
else if(estilo == 'carto-light') { style = [bright] }
else if(estilo == 'carto-dark' || window.matchMedia('(prefers-color-scheme: dark)').matches) { style = [dark] }
else { style = [bright] }

// Configuración del mapa
var mapa = L.map('mapa-linea', {
    center: [43.3445, -8.425],
    zoom: 12,
    scrollWheelZoom: 'center',
    doubleClickZoom: 'center',
    zoomSnap: 0.2,
    layers: style,
})

function onEachFeature(feature, layer) { if(feature.properties && feature.properties.popupContent) { layer.bindPopup(feature.properties.popupContent); } }

// Icono para las paradas
var stopIcon = L.icon({
    iconUrl: '/static/icons/maps/punto.png',

    iconSize: [8, 8],
    iconAnchor: [4, 4]
});
L.Marker.prototype.options.icon = stopIcon; // Hacer que el icono sea el que se utiliza por defecto
// Estilo de las líneas
var estiloLinea = {
    "color": "#5e31b1",
    "weight": 2,
    "opacity": 1
}

// Añadir los datos al mapa
mapa.addLayer(L.geoJson(paradas, { onEachFeature: onEachFeature })); // Paradas
mapa.addLayer(L.geoJson(linea, {onEachFeature: onEachFeature, style: estiloLinea }));   // Línea
mapa.fitBounds(L.geoJSON(paradas).getBounds());

// Calendarios
var date = new Date();  // Fecha para consultar los datos. Empieza siendo la actual

function calendario(accion) {
    // Modificar la fecha
    if(accion == 'mas') {
        date.setDate(date.getDate() + 1);
    }
    else if(accion == 'menos') {
        date.setDate(date.getDate() - 1);
    }

    cadena = date.getUTCFullYear().toString()+('0'+((date.getUTCMonth()+1).toString())).slice(-2)+date.getUTCDate().toString();  // Convertir la fecha a una cadena
    document.getElementById('fecha-consulta').innerHTML = date.getUTCDate().toString()+'/'+('0'+((date.getUTCMonth()+1).toString())).slice(-2)+'/'+date.getUTCFullYear().toString();    // Actualizar el indicador

    // Descargar los datos y actualizar la tabla
    if(accion == undefined && document.getElementById('horario-linea-ida').innerHTML != '') {
        // Evitar volver a descargar los datos si ya existen en una tabla
        return;
    }
    url = '/api/linea/'+window.location.pathname.split('/')[window.location.pathname.split('/').length-1]+'/salidas/'+cadena;
    fetch(url, {
        method: 'GET'
    })
    .then(function(response) { return response.json(); })
    .then(function(json) {
        const obj = json;   // Almacenar los datos en una variable
        ancho = 5;  // Número de columnas que tendrá la tabla

        // Generar las tablas
        if(obj.ida.length > 75) { ancho = 10; }
        document.getElementById('horario-linea-ida').innerHTML = tabla(obj.ida, ancho);
        document.getElementById('horario-linea-vuelta').innerHTML = tabla(obj.vuelta, ancho);

        // Generar la tabla a partir de los datos y el número de colunmas
        function tabla(datos, ancho) {
            if(datos.length == 0) {
                console.log('0')
                return 'Sin salidas';
            }
            var a = 0;
            var t = '';

            while(a < datos.length/ancho) {
                f = ''
                for(i=0; i<ancho; i++) {
                    var pos = i+a*ancho;
                    if(datos[pos] != undefined) { f += '<td>'+datos[pos]+'</td>'} else { break; }
                }
                a += 1;
                t += '<tr>'+f+'</tr>';
            }
            return t;
        }
    });
}

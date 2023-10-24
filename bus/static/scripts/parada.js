// Actualiza los próximos buses para una parada periódicamente y añade un mapa que muestra donde se encuentra la parada utilizando Leaflet-js

idioma = new URLSearchParams(window.location.search).get('lang');   // Guardar el idioma
estilo = new URLSearchParams(window.location.search).get('mapa');   // Guardar el estilo del mapa
// document.getElementById('msg-js').style.display = "none";   // Ocultar el error
document.getElementById('mapa-parada').innerHTML = '';  // Ocultar el error del mapa
actualizar(0);  // Actualizar al cargar la página
setInterval(function() { actualizar(last) }, 30000);    // Actualizar los datos cada 30s

// Buses
var last = new Date();
document.getElementById('boton-recarga').style.display = "";    // Mostrar el botón de actualización

function actualizar(last) {
    var now = new Date();

    if(now-last >= 15000) {
        window.last = now;

        // Descargar los datos y actualizar la información
        url = '/api/parada/'+window.location.pathname.substring(window.location.pathname.lastIndexOf('/')+1)+'/buses';
        fetch(url, {
            method: 'GET'
        })
        .then(function(response) { return response.json(); })
        .then(function(json) {
            const obj = json['buses']['lineas'];   // Almacenar los datos en una variable
            document.getElementById('lineas').innerHTML = '';   // Vaciar el contenedor

            // Iterar sobre las líneas
            for(i=0; i<obj.length; i++) {
                titulo = '<h1>'+cadenas[idioma][0]+' <span class="simbolo_linea" style="background-color: #'+obj[i].linea['color']+'">'+obj[i].linea['nombre']+'</span>'
                if(obj[i].linea['nombre'] == 'UDC') { titulo += ' <small style="font-size: 60%">(origen: '+obj[i].linea['origen']+')</small></h1>'; } else { titulo += '</h1>' }
                document.getElementById('lineas').innerHTML += titulo;
                for(b=0; b<obj[i].buses.length; b++) {
                    if(obj[i].buses[b].tiempo >= 60) {
                        ahora = new Date();
                        ahora.setMinutes(ahora.getMinutes()+parseInt(obj[i].buses[b].tiempo, 10));
                        hora = ahora.getHours()+':'+(ahora.getMinutes()<10?'0':'')+ahora.getMinutes();
                        if (obj[i].buses[b].distancia >= 1000) { distancia = Number(obj[i].buses[b].distancia/1000).toFixed(1); u='km'} else { distancia = obj[i].buses[b].distancia; u='m'}
                        linea = '<p>Bus '+obj[i].buses[b].bus+', a '+distancia+u+', '+hora+'.</p>';
                    }
                    else if(obj[i].buses[b].tiempo != 0) {
                        hora = obj[i].buses[b].tiempo;
                        if (obj[i].buses[b].distancia >= 1000) { distancia = Number(obj[i].buses[b].distancia/1000).toFixed(1); u='km'} else { distancia = obj[i].buses[b].distancia; u='m'}
                        linea = '<p>Bus '+obj[i].buses[b].bus+', a '+distancia+u+', '+hora+'\'.</p>';
                    }
                    else {
                        linea = '<p>Bus '+obj[i].buses[b].bus+', <b>'+cadenas[idioma][1]+'</b>.';
                    }
                    document.getElementById('lineas').innerHTML += linea;
                }
            }
            document.getElementById('t').innerHTML = cadenas[idioma][3]+': '+now.toLocaleString(cadenas[idioma][4]);
        });
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


// Mapa
var mapa = L.map('mapa-parada', {
    center: ubicacion,
    zoom: 17,
    dragging: false,
    boxZoom: false,
    zoomControl: false,
    scrollWheelZoom: 'center',
    doubleClickZoom: 'center',
    touchZoom: 'center',
    zoomDelta: 0.5,
    layers: style,
});

var circulo = L.circle(ubicacion, {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.25,
    radius: 7,
}).addTo(mapa);

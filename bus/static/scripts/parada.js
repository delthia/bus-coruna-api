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

var pin = 0;
function fijar(id_linea) {
    mostrar_chincheta(id_linea);
    if(pin == id_linea) {
        ocultar_chincheta(id_linea);
        pin = 0;
    }
    else {
        pin = id_linea;
    }
    mostrar_lineas(datos);
}

function mostrar_chincheta(id_linea) {
    document.getElementById('linea-'+id_linea).style.color = "var(--amarillo)";
    document.getElementById('linea-'+id_linea).style.display = "inline-block";
}
function ocultar_chincheta(id_linea) {
    document.getElementById('linea-'+id_linea).style.color = "";
    document.getElementById('linea-'+id_linea).style.display = "";
}

var datos;
function mostrar_lineas(obj, now) {
    document.getElementById('lineas').innerHTML = '';   // Vaciar el contenedor

    if(pin != 0) {
        for(p=0; p<obj.length; p++) {
            if(pin == obj[p].linea['id']) {
                break;
            }
        }
        pinned = [obj[p]];
        obj = pinned.concat(obj.slice(0, p), obj.slice(p+1, obj.length));
    }
    // Iterar sobre las líneas
    for(i=0; i<obj.length; i++) {
        // Nombre de la línea y origen en caso de que su nombre sea UDC
        if( obj[i].linea['nombre'] == 'UDC') { cierre = ' <small style="font-size: 60%">(origen: '+obj[i].linea['origen']+')</small>'; } else { cierre = ''; }

        document.getElementById('lineas').innerHTML += '<h1 onclick="fijar('+obj[i].linea['id']+')">'+cadenas[idioma][0]+' <span class="simbolo_linea" style="background-color: #'+obj[i].linea['color']+'">'+obj[i].linea['nombre']+'</span>'+cierre+'<span id="linea-'+obj[i].linea['id']+'" class="material-symbols-outlined stop_pin">push_pin</span></h1>';

        // Mostrar los buses para la línea
        buses = obj[i].buses
        for(j=0; j<buses.length; j++) {
            // Formatear la distancia
            if(buses[j].distancia >= 1000) {
                distancia = 'a '+Number(buses[j].distancia/1000).toFixed(1)+'km, ';
            }
            else {
                distancia = 'a '+buses[j].distancia+'m, ';
            }

            // Si el bus está a más de una hora, calcular la hora de llegada
            if(buses[j].tiempo >= 60) {
                ahora = new Date();
                ahora.setMinutes(ahora.getMinutes()+parseInt(buses[j].tiempo, 10));
                tiempo = ahora.getHours()+':'+(ahora.getMinutes()<10?'0':'')+ahora.getMinutes()+'.'
            }
            else if(buses[j].tiempo != 0) {
                tiempo = buses[j].tiempo+'\'.';
            }
            else {
                tiempo = '<b>'+cadenas[idioma][1]+'</b>.';
                distancia = '';
            }
            bus = '<p>Bus '+buses[j].bus+', '+distancia+tiempo;
            document.getElementById('lineas').innerHTML += bus;
        }
    }
    if(pin != 0) {mostrar_chincheta(pin); }
}

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
            datos = obj;
            mostrar_lineas(obj, now);
        });
    }
    else { flash_error(cadenas[idioma][2]); }
    document.getElementById('t').innerHTML = cadenas[idioma][3]+': '+now.toLocaleString(cadenas[idioma][4]);    
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

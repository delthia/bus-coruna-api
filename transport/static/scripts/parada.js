document.getElementById('boton-recarga').addEventListener('click', function(event) { actualizar(last); });
last = new Date();
// document.getElementById('alerta').style.display = "none";
document.getElementById('boton-recarga').style.display = "";

setInterval(function() {
    actualizar(last);
}, 30000);

// cadenas = {'es': ['Línea', 'en la parada', 'Aún no pasó el tiempo necesario', 'Última actualización', 'es-ES'], 'gal': ['Liña', 'na parada', 'Aínda non pasou o tempo necesario', 'Última actualización', 'es-ES'], 'en': ['Line', 'in the stop', 'Last update was too recently', 'Last updated on', 'en']};
idioma = new URLSearchParams(window.location.search).get('lang');

function actualizar(last) {
    right = new Date();
    if(right-last >= 15000) {
    // if(right-last >= 10) {
        window.last = right;
        id = document.getElementById('id-parada').innerHTML
    
        fetch('/api/parada/'+id, {
            method: 'GET'
        })
        .then(function(response) { return response.json(); })
        .then(function(json) {
            const obj = json;
            document.getElementById("lineas").innerHTML = '';
            for(i=0; i<obj['buses']['lineas'].length; i++) {
                console.log(obj['buses']['lineas'][i]);
                document.getElementById("lineas").innerHTML += '<h1>'+cadenas[idioma][0]+' <span class="simbolo_linea" style="background-color: #'+obj['buses']['lineas'][i].linea['color']+'">'+obj['buses']['lineas'][i].linea['nombre']+'</span></h1>';
                for(b=0; b<obj['buses']['lineas'][i].buses.length; b++) {
                    if(obj['buses']['lineas'][i].buses[b].tiempo >= 60) {
                        ahora = new Date();
                        ahora.setMinutes(ahora.getMinutes()+parseInt(obj['buses']['lineas'][i].buses[b].tiempo, 10));
                        hora = ahora.getHours()+':'+(ahora.getMinutes()<10?'0':'')+ahora.getMinutes();
                        document.getElementById("lineas").innerHTML += '<p>Bus '+obj['buses']['lineas'][i].buses[b].bus+', a '+obj['buses']['lineas'][i].buses[b].distancia+'m, '+hora+'.</p>';
                    }
                    else if (obj['buses']['lineas'][i].buses[b].tiempo != 0) {
                        hora = obj['buses']['lineas'][i].buses[b].tiempo;
                        document.getElementById("lineas").innerHTML += '<p>Bus '+obj['buses']['lineas'][i].buses[b].bus+', a '+obj['buses']['lineas'][i].buses[b].distancia+'m, '+hora+'\'.</p>';
                    }
                    else {
                        document.getElementById("lineas").innerHTML += '<p>Bus '+obj['buses']['lineas'][i].buses[b].bus+', <b>'+cadenas[idioma][1]+'</b>.';
                    }
                }
            }
            document.getElementById('t').innerHTML = cadenas[idioma][3]+': '+right.toLocaleString(cadenas[idioma][4]);
        })
    }
    else {
        document.getElementById('alerta').classList.add('alerta_visible');
        document.getElementById('alerta').innerHTML = cadenas[idioma][2];
        setTimeout(function() {
            document.getElementById('alerta').classList.remove('alerta_visible');
        }, 2500)
    }
}


if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    tiles = 'https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png';
}
else {
    tiles = 'https://c.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png';
    // tiles = 'https://c.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png';
}

// var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
document.getElementById('mapa-parada').innerHTML = '';

// Mapa de parada
var map = L.map('mapa-parada', {
    center: ubicacion,
    zoom: 18,
    dragging: false,
    boxZoom: false,
    scrollWheelZoom: 'center',
    zoomControl: false,
    doubleClickZoom: 'center',
    zoomDelta: 0.5,
});

var tiles = L.tileLayer(tiles, {
    maxZoom: 19,
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',
    minZoom: 17
}).addTo(map);

var circle = L.circle(ubicacion, {
    // color: '#280680',
    // fillcolor: '#5e35b1',
    color: 'red',
    fillColor: '#f03',
    // fillOpacity: 0.5,
    fillOpacity: 0.25,
    radius: 7
}).addTo(map);

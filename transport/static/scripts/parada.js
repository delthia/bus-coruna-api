document.getElementById('boton-recarga').addEventListener('click', function(event) { actualizar(last); });
last = new Date();
document.getElementById('alerta').style.display = "none";

setInterval(function() {
    actualizar(last);
}, 30000);

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
            // document.getElementById("todo").innerHTML = obj
            document.getElementById("lineas").innerHTML = '';
            for(i=0; i<obj['buses']['lineas'].length; i++) {
                console.log(obj['buses']['lineas'][i]);
                document.getElementById("lineas").innerHTML += '<h1>Línea <span class="simbolo_linea" style="background-color: #'+obj['buses']['lineas'][i].linea['color']+'">'+obj['buses']['lineas'][i].linea['nombre']+'</span></h1>';
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
                        document.getElementById("lineas").innerHTML += '<p>Bus '+obj['buses']['lineas'][i].buses[b].bus+', <b>en la parada</b>.';
                    }
                }
            }
            document.getElementById('t').innerHTML = 'Última actualización: '+right.toLocaleString('es-ES');
        })
    }
    else {
        document.getElementById('alerta').style.display = "";
        document.getElementById('alerta').innerHTML = 'Aún no pasó el tiempo necesario';
        setTimeout(function() {
            document.getElementById('alerta').innerHTML = '';
            document.getElementById('alerta').style.display = "none";
        },2500)
    }
}
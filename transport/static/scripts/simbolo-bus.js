document.getElementById('boton-recarga').addEventListener('click', function(event) { actualizar(last); });
last = new Date();
document.getElementById('msg-js').style.display = "none";

setInterval(function() {
    actualizar(last);
}, 30000)

function actualizar(last) {
    right = new Date();
    if(right-last >= 15000 || f == 't') {
        window.last = right;

        fetch('/api/linea/'+window.location.pathname.substring(window.location.pathname.lastIndexOf('/')+1)+'/buses', {
            method: 'GET'
        })
        .then(function(response) { return response.json(); })
        .then(function(json) {
            document.getElementById('buses-ida').innerHTML = '';
            document.getElementById('buses-vuelta').innerHTML = '';
            for(i=0;i<json['paradas'][0]['paradas'].length;i++) {
                // const altura = document.getElementById('ida').offsetHeight-35;
                const altura = document.getElementById('ida').offsetHeight-70;
                const x = (json['paradas'][0]['paradas'][i]['buses'][0]['distancia']*altura)+8;
                if(json['paradas'][0]['paradas'][i]['buses'][0]['estado'] == 0) {
                    document.getElementById('buses-ida').innerHTML += '<div style="margin-top: '+x+'px; position: absolute"><span class="material-symbols-outlined simbolo_bus simbolo_bus_parada">directions_bus</span></div>';
                }
                else if(json['paradas'][0]['paradas'][i]['buses'][0]['estado'] == 1) {
                    document.getElementById('buses-ida').innerHTML += '<div style="margin-top: '+x+'px; position: absolute"><span class="material-symbols-outlined simbolo_bus">directions_bus</span></div>';
                }
                else {
                    document.getElementById('buses-ida').innerHTML += '<div style="margin-top: '+x+'px; position: absolute"><span class="material-symbols-outlined simbolo_bus simbolo_bus_otro">directions_bus</span></div>';
                }
            }
            for(i=0;i<json['paradas'][0]['paradas'].length;i++) {
                // const altura = document.getElementById('vuelta').offsetHeight-35;
                const altura = document.getElementById('vuelta').offsetHeight-70;
                const x = (json['paradas'][1]['paradas'][i]['buses'][0]['distancia']*altura)+8;
                if(json['paradas'][1]['paradas'][i]['buses'][0]['estado'] == 0) {
                    document.getElementById('buses-vuelta').innerHTML += '<div style="margin-top: '+x+'px; position: absolute"><span class="material-symbols-outlined simbolo_bus simbolo_bus_parada">directions_bus</span></div>';
                }
                else if(json['paradas'][1]['paradas'][i]['buses'][0]['estado'] == 1) {
                    document.getElementById('buses-vuelta').innerHTML += '<div style="margin-top: '+x+'px; position: absolute"><span class="material-symbols-outlined simbolo_bus">directions_bus</span></div>';
                }
                else {
                    document.getElementById('buses-vuelta').innerHTML += '<div style="margin-top: '+x+'px; position: absolute"><span class="material-symbols-outlined simbolo_bus simbolo_bus_otro">directions_bus</span></div>';
                }
            }
            document.getElementById('t').innerHTML = 'Última actualización: '+right.toLocaleString('es-ES');
        })
    }
    else {
        document.getElementById('alerta').classList.add('alerta_visible');
        document.getElementById('alerta').innerHTML = 'Aún no pasó el tiempo necesario';
        setTimeout(function() {
            document.getElementById('alerta').classList.remove('alerta_visible');
        }, 2500)
    }
}

var f = 't';
actualizar(last);
var f = 'f';

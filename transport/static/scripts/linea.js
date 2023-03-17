document.getElementById('boton-recarga').addEventListener('click', function(event) { actualizar(last); });
last = new Date();
document.getElementById('alerta').style.display = "none";

setInterval(function() {
    actualizar(last);
}, 10000);

function actualizar(last) {
    right = new Date();
    if(right-last >= 500) {
        window.last = right;
        id = document.getElementById('id-linea').innerHTML
        
        fetch('/api/linea/'+id+'/buses', {
            method: 'GET'
        })
        .then(function(response) { return response.json(); })
        .then(function(json) {
            const obj = json;
            b = '';
            // https://bobbyhadz.com/blog/javascript-remove-all-elements-with-class
            const e = document.querySelectorAll('.info-bus');
            e.forEach(box => {
                box.remove();
            })
            for(i=0; i<obj['paradas'][1]['paradas'].length; i++) {
                console.log(obj['paradas'][1]['paradas'][i]['buses'][0]);
                b += '<div class="info-bus" style="margin-top:'+parseFloat(obj['paradas'][1]['paradas'][i]['buses'][0]['distancia'],10)*100+'%"><span class="material-symbols-outlined simbolo_bus">directions_bus</span><br><small style="text-align: center; display: block">'+obj['paradas'][1]['paradas'][i]['buses'][0]['bus']+'</small></div>';
            }
            document.getElementById('vuelta').innerHTML = b + document.getElementById('vuelta').innerHTML;
        })
    }
}

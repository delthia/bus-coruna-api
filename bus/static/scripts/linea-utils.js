function icono_bus(datos, sentido) {
    document.getElementById('buses-'+sentido).innerHTML = '';

    if(typeof(datos['paradas']) != undefined) {
        for(i=0; i<datos.length; i++) {
            var bus = datos[i]['buses'][0];
            const ajuste = -70;    // Offset de la altura
            const altura = document.getElementById(sentido).offsetHeight+ajuste;
            const posicion = bus['distancia']*altura+8;    // Posición del icono

            // Clases para los estilos del icono
            if(bus['estado'] == 0) {
                clase = ' simbolo_bus_parada ';
            }
            else if(bus['estado'] == 1) {
                clase = ' ';
            }
            else {
                clase = ' simbolo_bus-otro ';
            }
            document.getElementById('buses-'+sentido).innerHTML += '<div style="margin-top: '+posicion+'px; position: absolute"><span class="material-symbols-outlined simbolo_bus'+clase+'">directions_bus</span></div>';
        }
    }
}

function actualizar_diagrama(id_linea) {
    url = '/api/linea/'+id_linea+'/buses';

    fetch(url, {
        method: 'GET'
    })
    .then(function(response) { return response.json(); })
    .then(function(json) {
        const obj = json['paradas']
        // Actualizar los iconos
        icono_bus(obj[0], 'ida');
        icono_bus(obj[1], 'vuelta');
    })
}

function actualizar_mapa(id_linea) {
    url = '/api/linea/'+id_linea+'/buses/geo';

    fetch(url, {
        method: 'GET'
    })
    .then(function(response) {
        const obj = response.json()

        // Probar a eliminar la capa de buses
        try {
            mapa.removeLayer(geobuses);
        }
        catch {
            console.log('No eliminar la capa cuando aún no existe');
        }
        // geobuses = L.geoJson(obj).addTo(mapa);
    })
}

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
                for(i=0; i<5; i++) {
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

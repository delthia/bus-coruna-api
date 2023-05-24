function flash_error(mensaje) {
    // Reiniciar la clase de los elementos animables
    document.getElementById('mensaje-error').classList.remove('animar');
    document.getElementById('borde-abajo').classList.remove('animar');
    // Empezar la animación
    setTimeout(function() {
        document.getElementById('mensaje-error-mensaje').innerHTML = mensaje;
        document.getElementById('mensaje-error').classList.add('animar');
        document.getElementById('borde-abajo').classList.add('animar');
    }, 250);
}

// Estilos para los mapas
var bright = ['https://d.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://osm.ogr/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',
    minZoom: 13
}];

var dark = ['https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://osm.ogr/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',
    minZoom: 13
}];

var osm = ['https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://osm.ogr/copyright">OpenStreetMap</a>',
    minZoom: 13
}];

var pnoa = ['https://tms-pnoa-ma.idee.es/1.0.0/pnoa-ma/{z}/{x}/{-y}.jpeg', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://pnoa.ign.es">PNOA</a>, <a href="https://idee.es">IDEE</a>',
    minZoom: 13
}];

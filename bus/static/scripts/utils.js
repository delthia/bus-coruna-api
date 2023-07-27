// Mensajes de error
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

// Definir los estilos
osm = L.tileLayer(osm[0], osm[1]);
pnoa = L.tileLayer(pnoa[0], pnoa[1]);
bright = L.tileLayer(bright[0], bright[1])
dark = L.tileLayer(dark[0], dark[1])

// Cadenas para traducir los mensajes del resto de scripts
cadenas = {
    'es': ['Línea', 'en la parada', 'Aún no pasó el tiempo necesario', 'Última actualización', 'es-ES'],
    'gal': ['Liña', 'na parada', 'Aínda non pasou o tempo necesario', 'Última actualización', 'es-ES'],
    'en': ['Line', 'in the stop', 'Last update was too recently', 'Last updated on', 'en']
};

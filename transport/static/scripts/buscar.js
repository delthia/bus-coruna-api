search = new URLSearchParams(window.location.search).get('search');

document.getElementById('buscar').style.display = "";
document.getElementById('buscar').value = search;

function buscar() {
    var input, filter, table, tr, i
    input = document.getElementById("buscar");
    filter = input.value.toUpperCase();
    table = document.getElementById("paradas");
    tr = table.getElementsByTagName("tr");

    for(i=0; i<tr.length; i++) {
        id = tr[i].getElementsByTagName("td")[0];
        nombre = tr[i].getElementsByTagName("td")[1];

        if(id) {
            t = id.textContent || id.innerText;
            n = nombre.textContent || nombre.innerText;
            if(t.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            }
            else if(n.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            }
            else {
                tr[i].style.display = "none";
            }
        }
    }
}

$(document).ready(function(){
    let date = new Date();
    let today = date.getFullYear() + "-" + ("0" + (date.getMonth() + 1)).slice(-2) + "-" + ("0" + date.getDate()).slice(-2);
    document.getElementById("fecha-termino").setAttribute("min", today);
    updatePoints();
})

function minDate() {
    let inputObj = document.getElementById("fecha-termino");
    let today = new Date();
    today.setHours(0,0,0,0);
    let dateSplit = inputObj.value.split('-');
    let input = new Date(dateSplit[0], dateSplit[1] - 1, dateSplit[2]);
    if (input.getTime() < today.getTime()) {
        today = today.getFullYear() + "-" + ("0" + (today.getMonth() + 1)).slice(-2) + "-" + ("0" + today.getDate()).slice(-2)
        document.getElementById("fecha-termino").value = today;
    }
}

function updatePoints() {
    let puntosElement = $('#puntos')[0]
    let puntosTotales = puntosElement.value;
    let respNes = $('#respuestas-necesarias')[0].value;
    if (respNes == 0){
        $('#puntos-x-resp')[0].innerHTML = 'Se darán - puntos por respuesta.';
    } else {
        let basepoints = $('#puntos-x-resp')[0].dataset.basepoints
        $('#puntos-x-resp')[0].innerHTML = 'Se darán ' + (Math.floor(puntosTotales/respNes) + Number(basepoints)) + ' puntos por respuesta.';
    }
}
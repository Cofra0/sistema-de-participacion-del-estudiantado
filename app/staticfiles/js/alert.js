/*JavaScript para alertar al usuario si no ha respondido la encuesta*/
console.log("cargo al menos");
window.onbeforeunload = function() {
    console.log("en la functionnnnnnnnnnnnn");
    const respondido = document.getElementById("respondido");
    if (!(respondido)) {
        return "Aún no has respondido correctamente la encuesta. ¿Deseas salir de todas maneras?";
    }
}
/*JavaScript para alertar al usuario si no ha respondido la encuesta*/
const confirmationMessage = "Aún no se ha respondido la encuesta correctamente." + 
 "¿Deseas salir de todas maneras?";
let respondido = document.getElementById("respondido");
respondido = respondido.value === "True";
/*
Seleccionamos todos los tags 'a' y le agregamos una función que maneje
si la encuesta fue respondida o no
*/
document.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', (e) => {
        if (!respondido) {
            const res = window.confirm(confirmationMessage);
            if (!res) { //Si el cliente cancela la salida a la página, se cancela el redirect
                e.preventDefault();
            }
        }
    });
  });
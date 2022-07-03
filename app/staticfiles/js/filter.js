function filterByAnswered(event) {
    const value = event.target.value; //Valor para filtrar
    console.log(value);
    let encuestas = document.getElementsByClassName("encuesta");
    let number = 1;
    for (encuesta of encuestas) { //Iteramos sobre las encuestas
        const answered = (encuesta.querySelector(".poll_answered")).innerHTML; //Obtenemos si es respondida o no
        let rank = (encuesta.querySelector(".poll_rank"));
        if (value === "All") {
            encuesta.style.display = "table-row";
            rank.innerHTML = number++;
        } else if ((value === "Not Answered" && answered === "False") || (value === "Answered" && answered === "True")) {
            encuesta.style.display = "table-row";
            rank.innerHTML = number++;
        } else { //No hay que mostrar el elemento
            encuesta.style.display = "none";
        }
    }
}
function validate() {
    let nombre = document.getElementById("nombre");
    let descripcion = document.getElementById("descripcion");
    let puntos = document.getElementById("puntos");
    let numRespuestas = document.getElementById("respuestas-necesarias");
    let fechaTermino = document.getElementById("fecha-termino");
    let horaTermino = document.getElementById("hora-termino");
    let numPreguntas = document.getElementById("numero-preguntas");
    let linkEncuesta = document.getElementById("link-encuesta");
    let codigoEncuesta = document.getElementById("codigo-encuesta");

    let state = true;

    let error = document.getElementById("error-nombre");
    let div = document.getElementById("nombre");
    if (nombre.value == '') {
        error.innerHTML = 'Se debe ingresar un nombre para la encuesta.';
        div.classList.add("is-invalid");
        state = false;
    } 
    else if (!(5 <= nombre.value.length <= 80)) {
        error.innerHTML = 'El nombre debe tener entre 5 y 80 caracteres.';
        div.classList.add("is-invalid");
        state = false;
    }
    else {
        div.classList.remove("is-invalid");
    }

    error = document.getElementById("error-descripcion");
    div = document.getElementById("descripcion");
    if (descripcion.value == '') {
        error.innerHTML = 'Se debe ingresar una descripción para la encuesta';
        div.classList.add("is-invalid");
        state = false;
    }
    else if (descripcion.value.length < 5) {
        error.innerHTML = 'La descripción debe tener mínimo 5 caracteres.';
        div.classList.add("is-invalid");
        state = false;
    }
    else {
        error.innerHTML = '';
        div.classList.remove("is-invalid");
    }

    error = document.getElementById("error-puntos");
    div = document.getElementById("puntos");
    if (puntos.value == '' || isNaN(puntos.value) || !Number.isInteger(Number(puntos.value)) || Number(puntos.value) < 0) {
        error.innerHTML = 'Se debe ingresar un número entero positivo';
        div.classList.add("is-invalid");
        state = false;
    } 
    else if (puntos.value > puntos.max) {
        error.innerHTML = 'Puntos superan el máximo disponible.';
        div.classList.add("is-invalid");
        state = false;
    }
    else {
        error.innerHTML = '';
        div.classList.remove("is-invalid");
    }

    error = document.getElementById("error-respuestas-necesarias");
    div = document.getElementById("respuestas-necesarias");
    if (numRespuestas.value == '' || isNaN(numRespuestas.value) || !Number.isInteger(Number(numRespuestas.value)) || Number(numRespuestas.value) < 0) {
        error.innerHTML = 'Se debe ingresar un número entero positivo';
        div.classList.add("is-invalid");
        state = false;
    } else {
        error.innerHTML = '';
        div.classList.remove("is-invalid");
    }

    error = document.getElementById("error-fecha-termino");
    div = document.getElementById("fecha-termino");
    if (fechaTermino.value == '') {
        error.innerHTML = 'Se debe ingresar una fecha de término';
        error.style.display = 'block'
        div.classList.add("is-invalid");
        state = false;
    } else {
        let date = new Date();
        date.setHours(0,0,0,0);
        try {
            let dateSplit = fechaTermino.value.split('-');
            let inputDate = new Date(dateSplit[0], dateSplit[1] - 1, dateSplit[2]);
            if (inputDate < date) {
                error.innerHTML = 'La fecha de término no puede ser anterior a hoy';
                error.style.display = 'block'
                div.classList.add("is-invalid");
                state = false;
            } else {
                error.innerHTML = '';
                div.classList.remove("is-invalid");
            }
        }
        catch (e) {
            error.innerHTML = 'La fecha no tiene el formato permitido';
            error.style.display = 'block'
            div.classList.add("is-invalid");
            state = false;
        }
    }

    error = document.getElementById("error-hora-termino");
    div = document.getElementById("hora-termino");
    if (horaTermino.value == '') {
        error.innerHTML = '';
        div.classList.remove("is-invalid");
    } else {
        let date = new Date();
        let todayDate = date.getFullYear() + "-" + ("0" + (date.getMonth() + 1)).slice(-2) + "-" + ("0" + date.getDate()).slice(-2);
        let now = ("00" + date.getHours()).slice(-2) + ":" + ("00" + date.getMinutes()).slice(-2);
        if (todayDate == fechaTermino.value && horaTermino.value < now) {
            error.style.display = 'block'
            error.innerHTML = 'Hora de término inválida (es anterior a ahora).';
            div.classList.add("is-invalid");
            state = false;
        } else {
            error.innerHTML = '';
            div.classList.remove("is-invalid");
        }
    }

    error = document.getElementById("error-numero-preguntas");
    div = document.getElementById("numero-preguntas");
    if (numPreguntas.value == '' || isNaN(numPreguntas.value) || !Number.isInteger(Number(numPreguntas.value)) || Number(numPreguntas.value) < 0) {
        error.innerHTML = 'Se debe ingresar un número entero positivo';
        div.classList.add("is-invalid");
        state = false;
    } else {
        div.classList.remove("is-invalid");
    }


    error = document.getElementById("error-link-encuesta");
    div = document.getElementById("link-encuesta");
    if (linkEncuesta.value == '') {
        error.innerHTML = 'Se debe ingresar una url a una encuesta.';
        div.classList.add("is-invalid");
        state = false;
    } 
    else {
        let url = linkEncuesta.value;
        shortUrl = /^https:\/\/forms.gle\/([\w-]){17}$/;
        longUrl = /^https:\/\/docs.google.com\/forms\/d\/e\/[\w-]{56}\/viewform(\?usp=sf_link)?$/;
        if (longUrl.test(url) || shortUrl.test(url)) {
            const req = new XMLHttpRequest();
            const reqUrl = '/val_url/' + url;
            req.open('GET', reqUrl, false);
            req.onload = function(){
                let param = req.response;
                dic = JSON.parse(param);
                let statusCode = Number(dic.status);
                if (statusCode !== 200) {
                    error.innerHTML = 'La url no es válida.';
                    div.classList.add("is-invalid");
                    state = false;
                } else {
                    div.classList.remove("is-invalid");
                }
            }
            req.send();
        }
        else {
            error.innerHTML = 'La url no corresponde a una encuesta de google forms.';
            div.classList.add("is-invalid");
            state = false;
        }
    }

    error = document.getElementById("error-codigo-encuesta");
    div = document.getElementById("codigo-encuesta");
    if (codigoEncuesta.value == '') {
        error.innerHTML = 'Se debe ingresar el código de verificación de respuesta.';
        div.classList.add("is-invalid");
        state = false;
    }
    else {
        error.innerHTML = '';
        div.classList.remove("is-invalid");
    }
    
    return state;
}
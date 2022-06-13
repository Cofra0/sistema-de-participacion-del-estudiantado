let user_name = document.getElementById("user_name");
    
user_name.onclick = function(){

    let close_session = document.getElementById("close_session");
    let arrow = document.getElementById("arrow");
    

    if (close_session.className == "close_session"){
        close_session.classList.replace("close_session", "close_session_nv");
        arrow.style.transform = "rotate(0deg)";
        user_name.style.background = "#d1cb85";
    }

    else{
        close_session.classList.replace("close_session_nv", "close_session" );
        arrow.style.transform = "rotate(180deg)";
        user_name.style.background = "#a9a46c";
    }
};


let en = document.getElementById("encuestas");
let mien = document.getElementById("mis_encuestas");
let puen = document.getElementById("publicar");

/* Muestra info de como reportar */
function reportar() {
    let modal = document.getElementById("reportar-info");
    modal.style.display = "block";
}

/* Cierra la info de como reportar */
function cerrar() {
    let modal1 = document.getElementById("reportar-info");
    modal1.style.display = "none";
}
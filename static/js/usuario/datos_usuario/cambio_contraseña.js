function VerContraseña(evento) {
    if (evento.tagName == "I") {
        boton = evento.parentElement;
    } else {
        boton = evento;
    }

    if (boton.parentElement.children[1].type == "password") {
        boton.parentElement.children[1].type = 'text';
    } else {
        boton.parentElement.children[1].type = "password";
    }

    if (boton.parentElement.children[2].children[0].className == "bi bi-eye-fill") {
        boton.parentElement.children[2].children[0].className = 'bi bi-eye-slash-fill';
    } else {
        boton.parentElement.children[2].children[0].className = "bi bi-eye-fill";
    }
    
    }

$(document).on('click', '.btn-info', function (e) {
    VerContraseña(e.target);
});


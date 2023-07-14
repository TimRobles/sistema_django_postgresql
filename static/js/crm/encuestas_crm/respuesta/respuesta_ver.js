respuesta = $('#respuesta_id')[0].innerHTML;
url = $('#url')[0].innerHTML;
function responder() {
    datos = new FormData();
    datos.append('respuesta', respuesta);
    $respuesta_opcion = document.getElementsByClassName('respuesta-opcion-crm');
    grupo = Array();
    for (let index = 0; index < $respuesta_opcion.length; index++) {
        const element = $respuesta_opcion[index];
        if (element.checked) {
            console.log(element);
            console.log(element.checked);
            alternativa = element.dataset['alternativa'];
            pregunta = element.dataset['pregunta'];
            texto = '';
            borrador = true;
            
            fila = Array();
            fila.push(alternativa);
            fila.push(pregunta);
            fila.push(borrador);
            datos.append('opcion-' + index, fila);
        }
    }

    $respuesta_alternativa = document.getElementsByClassName('respuesta-alternativa-crm');
    grupo = Array();
    for (let index = 0; index < $respuesta_alternativa.length; index++) {
        const element = $respuesta_alternativa[index];
        if (element.checked) {
            console.log(element);
            console.log(element.checked);
            alternativa = element.dataset['alternativa'];
            pregunta = element.dataset['pregunta'];
            texto = '';
            borrador = true;
            
            fila = Array();
            fila.push(alternativa);
            fila.push(pregunta);
            fila.push(borrador);
            datos.append('alternativa-' + index, fila);
        }
    }

    $respuesta_texto = document.getElementsByClassName('respuesta-texto-crm');
    grupo = Array();
    for (let index = 0; index < $respuesta_texto.length; index++) {
        const element = $respuesta_texto[index];
        if (element.value) {
            console.log(element);
            alternativa = '';
            pregunta = element.dataset['pregunta'];
            texto = element.value;
            borrador = true;
            
            fila = Array();
            fila.push(pregunta);
            fila.push(borrador);
            fila.push(texto);
            datos.append('texto-' + index, fila);
        }
    }
    console.log(datos);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = xhr.responseText;
        }else{
            $respuesta = false;
        }
    }
    xhr.send(datos);

    Swal.fire({
        title: "Gracias por llenar la encuesta",
        text: "Te estamos enviando a una página bonita",
        icon: "success",
      });
    
    setTimeout(() => {
        location.href = 'https://www.multiplay.com.pe/';
    }, 5000);
}
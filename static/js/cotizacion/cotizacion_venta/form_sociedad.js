inputs = document.getElementsByTagName('input')

function inicio() {
    cantidades = document.getElementById('cantidades').innerHTML;
    for (let index = 2; index < inputs.length-1; index++) {
        const element = inputs[index];
        element.value = cantidades.split('|')[index-2]
    }
}

function calcular() {
    var contador = 0;
    var suma = 0;
    for (let index = 1; index < inputs.length; index++) {
        const element = inputs[index];
        contador++;
        if (contador == 1) {
            if (element.value != "") {
                cantidad = parseInt(element.value);
            } else {
                cantidad = 0;
            }
        }else if (contador == inputs.length-1) {
            // Nada
        }else {
            if (element.value != "") {
                suma = suma + parseInt(element.value);
            } else {
                suma = suma + 0;
            }
        }
    }
    pendiente = cantidad - suma;
    inputs[inputs.length-1].value = pendiente;
}

for (let index = 1; index < inputs.length; index++) {
    const element = inputs[index];
    element.addEventListener('input', calcular);
}

$('#modal').unbind().on('shown.bs.modal', function (e) {
    inicio();
    calcular();
});

function guardar() {
    url = $('#url_guardar')[0].innerHTML;
    var contador = 0;
    for (let index = 1; index < inputs.length; index++) {
        const element = inputs[index];
        contador++;
        if (contador == 1) {
            // Nada
        }else if (contador == inputs.length-1) {
            // Nada
        }else {
            if (element.value != "") {
                cantidad = parseInt(element.value);
            } else {
                cantidad = 0;
            }
            item = element.name;
            sociedad = element.id;
            url_final = url + cantidad + '/' + item + '/' + sociedad + '/'
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url_final);
            xhr.onload = function(){
                if (this.status === 200) {
                    setTimeout(() => {
                        inicio();
                        calcular();
                    }, 1000);
                }
            }
            xhr.send();
        }
    }
}

$('#guardar_formulario').unbind().on('click', function (e) {
    guardar();
});
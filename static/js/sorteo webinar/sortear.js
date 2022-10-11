function randomText(datos) {
    min = 0;
    max = Object.keys($datos).length - 1;
    console.log(Math.floor(Math.random() * (max - min + 1)) + min)
    return datos[Math.floor(Math.random() * (max - min + 1)) + min]['nombre'];
}

function ruleta(element, tiempo, final, datos) {
    var girar = setInterval(() => {
        element.innerHTML = randomText(datos);
    }, 100);
    setTimeout(() => {
        clearInterval(girar);
        element.innerHTML = final
    }, tiempo*1000);
}

function sorteo(respuesta, tiempo) {
    setTimeout(() => {
        Swal.fire({
            title: respuesta.split(" | ")[1],
            html: respuesta.split(" | ")[2],
          });
    }, tiempo*1000 + 500);
}

$('#sortear').on('click', function (e) {
    var nombre = $('#nombre')[0];
    
    url = '/sorteo-webinar/datos/';
    
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $datos = JSON.parse(xhr.responseText);
            console.log($datos[0]);
            console.log($datos[0]['nombre']);
            console.log(Object.keys($datos).length);

            url_nested = '/sorteo-webinar/sortear/';
    
            var xhr_nested = new XMLHttpRequest();
            xhr_nested.open('GET', url_nested);
            xhr_nested.onload = function(){
                if (this.status === 200) {
                    console.log(xhr_nested.responseText);
                    tiempo = 10;
                    ruleta(nombre, tiempo*1, xhr_nested.responseText.split(" | ")[0], $datos);
                    sorteo(xhr_nested.responseText, tiempo+1)
                }
            }
            xhr_nested.send();
        }
    }
    xhr.send();
})
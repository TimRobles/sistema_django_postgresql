function randomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function ruleta(element, tiempo, final) {
    var girar = setInterval(() => {
        element.innerHTML = randomInteger(0, 9);
    }, 50);
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
    var primero = $('#primero')[0];
    var segundo = $('#segundo')[0];
    var tercero = $('#tercero')[0];
    var cuarto = $('#cuarto')[0];
    
    url = '/sorteo/sortear/';
    
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            console.log(xhr.responseText);
            tiempo = 2;
            ruleta(primero, tiempo*1, xhr.responseText.charAt(0));
            ruleta(segundo, tiempo*2, xhr.responseText.charAt(1));
            ruleta(tercero, tiempo*3, xhr.responseText.charAt(2));
            ruleta(cuarto, tiempo*4, xhr.responseText.charAt(3));
            sorteo(xhr.responseText, tiempo*4)
        }
    }
    xhr.send();
})
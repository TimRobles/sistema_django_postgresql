function envioAjax(datos, url){
    var xhr = new XMLHttpRequest();
    xhr.open('POST',url, true);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send(datos);
};


var respuesta = document.getElementById('respuesta').value;
var url = document.getElementById('url').value;
var url2 = document.getElementById('url2').value;

$('#enviar').on('click', function(e) {
    e.preventDefault();
    for (let i = 1; i < e.target.parentElement.length; i++) {
        
        const element = e.target.parentElement[i];
        
        let pregunta = element.getAttribute('name');
        let alternativa = element.value;
        let texto = element.value;
        
        


        if (element.getAttribute('type')=='text') {
            datos = new FormData();
            datos.append('respuesta', respuesta);
            datos.append('pregunta', pregunta);
            datos.append('alternativa', '');
            datos.append('texto', texto);
            envioAjax(datos, url);

        } 
        else if(element.getAttribute('type')=='hidden') {
            
        }
        else if(element.getAttribute('type')=='submit') {
            
        }
        else {
            if (element.checked) {
                datos = new FormData();
                datos.append('respuesta', respuesta);
                datos.append('pregunta', pregunta);
                datos.append('alternativa', alternativa);
                datos.append('texto', '');
                envioAjax(datos, url);

            }
        }
        
    }
    setTimeout(() => {
        window.location.href = url2;
    }, 1000);
})


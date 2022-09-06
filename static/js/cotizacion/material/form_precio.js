function seleccionar_comprobante(valores) {
    if (valores != "") {
        
        valores2 = valores.split('|');
        
        $id_comprobante = valores2[0]
        $comprobante_content_type = valores2[1]
        $id_material = valores2[2]
        $material_content_type = valores2[3]
        
        $precio_compra = $('#id_precio_compra')[0];
        $moneda = $('#id_moneda')[0];
        $logistico = $('#id_logistico')[0];
        
        
        url = '/material/precio-material/' + $id_comprobante + '/' + $comprobante_content_type + '/' + $id_material + '/' + $material_content_type + '/';
        console.log(url);
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.onload = function(){
            if (this.status === 200) {
                valores3 = xhr.responseText.split('|');
                console.log($moneda)
                
                $precio_compra.value = valores3[0]
                setSelectedValueText($moneda,valores3[1]);
                $logistico.value = valores3[2];
            }
        }
        xhr.send();
    }
}

function calcular_precio_lista() {
    $margen_venta =$('#id_margen_venta')[0].value;
    $precio_compra = $('#id_precio_compra')[0].value;
    $logistico = $('#id_logistico')[0].value;

    $precio_lista = $('#id_precio_lista')[0];
    
    $precio_lista.value = Math.round(10000000000*$precio_compra*$logistico*$margen_venta)/10000000000;
    
    console.log($precio_lista.value);
    
}

function calcular_margen_venta() {
    $precio_compra = $('#id_precio_compra')[0].value;
    $logistico = $('#id_logistico')[0].value;
    $precio_lista = $('#id_precio_lista')[0].value;
    
    $margen_venta = $('#id_margen_venta')[0];

    $margen_venta.value = Math.round(10000000000*$precio_lista/($precio_compra*$logistico))/10000000000;

    console.log($margen_venta);
    
}

function calcular_precio_sin_igv() {
    $precio_lista = $('#id_precio_lista')[0].value;
    $valor_igv = 0.18
    $precio_sin_igv = $('#id_precio_sin_igv')[0];

    $precio_sin_igv.value = Math.round(($precio_lista/(1 + $valor_igv))*10000000000)/10000000000;
    console.log($precio_sin_igv);
}


$('#id_comprobante').on('change', function (e) {
    seleccionar_comprobante(e.target.value);
    setTimeout(() => {
        calcular_precio_lista();
        calcular_precio_sin_igv();
    }, 100);
});

$('#id_logistico').on('input', function (e) {
    console.log(e.target.value);
    calcular_precio_lista();
    calcular_precio_sin_igv();
});

$('#id_margen_venta').on('input', function (e) {
    console.log(e.target.value);
    calcular_precio_lista();
    calcular_precio_sin_igv();
});

$('#id_precio_lista').on('input', function (e) {
    console.log(e.target.value);
    calcular_margen_venta();
    calcular_precio_sin_igv();
});

seleccionar_comprobante($('#id_comprobante')[0].value);
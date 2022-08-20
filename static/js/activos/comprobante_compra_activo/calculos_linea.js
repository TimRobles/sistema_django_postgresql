function CalculosLinea() {
    click_habilitar(true);
    $tipo_igv = $('#id_tipo_igv')[0].value;
    if ($tipo_igv == 1) {
        $valor_igv = 0.18
    } else {
        $valor_igv = 0.00
    }
    
    $cantidad = $('#id_cantidad')[0].value;
    $precio_unitario_con_igv = $('#id_precio_unitario_con_igv')[0].value;
    $precio_unitario_sin_igv = $('#id_precio_unitario_sin_igv')[0];
    $precio_final_con_igv= $('#id_precio_final_con_igv')[0].value;
    $descuento = $('#id_descuento')[0];
    $sub_total = $('#id_sub_total')[0];
    $igv = $('#id_igv')[0];
    $total = $('#id_total')[0];

    url = '/calculo-item-linea/' + $cantidad + "/" + $precio_unitario_con_igv + "/" + $precio_final_con_igv + "/" + $valor_igv;

    console.log(url);
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            $info = JSON.parse($respuesta['info'].replace(/&quot;/g,'"').replace(/&amp;/g,'&'));

            $precio_unitario_sin_igv.value = $info['precio_unitario_sin_igv'];
            $descuento.value = $info['descuento'];
            $sub_total.value = $info['subtotal'];
            $igv.value = $info['igv'];
            $total.value = $info['total'];

        }else{
            $respuesta = false;
            $precio_unitario_sin_igv.value = "";
            $descuento.value = "";
            $sub_total.value = "";
            $igv.value = "";
            $total.value = "";
        }
    }
    xhr.send();
}

$('#id_cantidad').on('input', function (e) {
    console.log(e.target.value);
    CalculosLinea();
});
$('#id_precio_unitario_con_igv').on('input', function (e) {
    console.log(e.target.value);
    CalculosLinea();
});
$('#id_precio_final_con_igv').on('input', function (e) {
    console.log(e.target.value);
    CalculosLinea();
});
$('#id_tipo_igv').on('input', function (e) {
    console.log(e.target.value);
    CalculosLinea();
});

function click_habilitar (valor) {
    $('#id_precio_unitario_sin_igv')[0].disabled = valor;
    $('#id_precio_unitario_sin_igv')[0].disabled = valor;
    $('#id_descuento')[0].disabled = valor;
    $('#id_sub_total')[0].disabled = valor;
    $('#id_igv')[0].disabled = valor;
    $('#id_total')[0].disabled = valor;
};

$(document).on("click", ".btn-primary", function (e) {
    click_habilitar(false);
});

CalculosLinea();
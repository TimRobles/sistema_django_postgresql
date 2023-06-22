function tipo_cambio() {
    $total_documento = $('#id_total_documento')[0].value-0;
    $tipo_cambio = $('#id_tipo_cambio')[0].value-0;
    $total_requerimiento = Math.round(($total_documento * $tipo_cambio)*100)/100;
    $('#id_total_requerimiento')[0].value = $total_requerimiento;
    $('#id_total_requerimiento')[0].disabled = true;
}

function cambio_moneda() {
    $moneda = $('#id_moneda')[0].value;
    $moneda_requerimiento = $('#id_moneda_requerimiento')[0].value;
    if ($moneda) {
        if ($moneda == $moneda_requerimiento) {
            $('#id_tipo_cambio')[0].value = 1;
            $('#id_tipo_cambio')[0].disabled = true;
        }else{
            $('#id_tipo_cambio')[0].disabled = false;
        }
    }else{
        $('#id_tipo_cambio')[0].disabled = true;
    }
}

$(document).on("input", "#id_tipo_cambio", function () {
    tipo_cambio();    
});

$(document).on("input", "#id_total_documento", function () {
    tipo_cambio();    
});

$(document).on("change", "#id_moneda", function () {
    cambio_moneda();
    tipo_cambio();
});

function click_habilitar (valor) {
    $('#id_total_requerimiento')[0].disabled = valor;
    $('#id_tipo_cambio')[0].disabled = valor;
    $('#id_moneda_requerimiento')[0].disabled = valor;
};

$(document).on("click", ".btn-primary", function (e) {
    click_habilitar(false);
    setTimeout(() => {
        click_habilitar(true);
    }, 2000);
});

cambio_moneda();
tipo_cambio();
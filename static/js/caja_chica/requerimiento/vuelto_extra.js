function calculo() {
    $vuelto_original = $('#id_vuelto_original')[0].value-0;
    $vuelto_extra = $('#id_vuelto_extra')[0].value-0;
    $moneda = $('#id_moneda')[0].value;
    if ($vuelto_extra) {
        if ($moneda == 2) { // Dólares
            $tipo_cambio = Math.round(($vuelto_extra / $vuelto_original)*10000)/10000;
        } else {
            $tipo_cambio = Math.round(($vuelto_original / $vuelto_extra)*10000)/10000;
        }
        $('#id_tipo_cambio')[0].value = $tipo_cambio;
    }
    cambio_moneda();
}

function cambio_moneda() {
    $tipo_cambio = $('#id_tipo_cambio')[0];
    $vuelto_extra = $('#id_vuelto_extra')[0];
    $vuelto_original = $('#id_vuelto_original')[0].value-0;
    $moneda = $('#id_moneda')[0].value;
    $moneda_requerimiento = $('#id_moneda_requerimiento')[0].value;
    if ($moneda) {
        if ($moneda == $moneda_requerimiento) {
            $vuelto_extra.value = $vuelto_original
            $tipo_cambio.value = '1.00'
            $vuelto_extra.disabled = true
        }else{
            $vuelto_extra.disabled = false
        }
    }
    console.log($moneda, $moneda_requerimiento)
}

$(document).on("input", "#id_vuelto_original", function () {
    calculo();
});

$(document).on("input", "#id_vuelto_extra", function () {
    calculo();
});

$(document).on("change", "#id_moneda", function () {
    cambio_moneda();
});

function click_habilitar (valor) {
    $('#id_moneda_requerimiento')[0].disabled = valor;
    $('#id_tipo_cambio')[0].disabled = valor;
    $('#id_vuelto_extra')[0].disabled = valor;
};

$(document).on("click", ".btn-primary", function (e) {
    click_habilitar(false);
    setTimeout(() => {
        click_habilitar(true);
    }, 2000);
});

click_habilitar (true)
calculo();
function calculo() {
    $monto_final = $('#id_monto_final')[0].value-0;
    $tipo_cambio = $('#id_tipo_cambio')[0].value-0;
    $monto_entregado = Math.round(($monto_final * $tipo_cambio)*100)/100;
    $('#id_monto_entregado')[0].value = $monto_entregado;
}

$(document).on("input", "#id_monto_final", function () {
    calculo();
});

$(document).on("input", "#id_tipo_cambio", function () {
    calculo();
});

function click_habilitar (valor) {
    $('#id_monto_entregado')[0].disabled = valor;
};

$(document).on("click", ".btn-primary", function (e) {
    click_habilitar(false);
    setTimeout(() => {
        click_habilitar(true);
    }, 500);
});

click_habilitar (true)
calculo();
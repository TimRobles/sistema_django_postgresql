function calculo() {
    $monto_final = $('#id_monto_final')[0].value-0;
    $utilizado = $('#id_utilizado')[0].value-0;
    $redondeo = $('#id_redondeo')[0].value-0;
    $vuelto_extra = $('#id_vuelto_extra')[0].value-0;
    $vuelto = Math.round(($monto_final - $utilizado - $redondeo - $vuelto_extra)*100)/100;
    $('#id_vuelto')[0].value = $vuelto;
}

$(document).on("input", "#id_redondeo", function () {
    calculo();
});

function click_habilitar (valor) {
    $('#id_utilizado')[0].disabled = valor;
    $('#id_monto_final')[0].disabled = valor;
    $('#id_vuelto_extra')[0].disabled = valor;
    $('#id_vuelto')[0].disabled = valor;
};

$(document).on("click", ".btn-primary", function (e) {
    click_habilitar(false);
    setTimeout(() => {
        click_habilitar(true);
    }, 2000);
});

click_habilitar (true)
calculo();
function calculo() {
    $recibido = $('#id_recibido')[0].value-0;
    $monto_usado = $('#id_monto_usado')[0].value-0;
    $comision = $('#id_comision')[0].value-0;
    $redondeo = $('#id_redondeo')[0].value-0;
    $vuelto_extra = $('#id_vuelto_extra')[0].value-0;
    $vuelto = Math.round(($recibido - $monto_usado - $comision - $redondeo - $vuelto_extra)*100)/100;
    $('#id_vuelto')[0].value = $vuelto;
}

$(document).on("input", "#id_redondeo", function () {
    calculo();
});

function click_habilitar (valor) {
    $('#id_recibido')[0].disabled = valor;
    $('#id_monto_usado')[0].disabled = valor;
    $('#id_vuelto_extra')[0].disabled = valor;
    $('#id_comision')[0].disabled = valor;
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
function forma_pago(tipo) {
    forma = $('#forma')[0].innerHTML;
    if (tipo==1) {
        $('#id_condiciones_pago')[0].value = "";
        $('#id_condiciones_pago')[0].disabled = true;
    } else {
        $('#id_condiciones_pago')[0].value = forma;
        $('#id_condiciones_pago')[0].disabled = false;
    }
}

$('#id_tipo_venta').unbind().on('change', function (e) {
    forma_pago(e.target.value);
})
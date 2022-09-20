function calcular(e) {
    saldo = $('#saldo')[0];
    pendiente = $('#pendiente')[0];
    pendiente.value = saldo.value - e.value
}

$('#id_monto').unbind().on('input', function (e) {
    calcular(e.target);
})

calcular($('#id_monto')[0]);
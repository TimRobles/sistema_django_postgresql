function seleccionar_ingresos(ingresos) {
    texto = getSelectedValueText(ingresos, ingresos.value);
    textos = texto.split(' ');
    texto_monto_final = monto_final.parentElement.children[0];
    if (textos.length > 1) {
        moneda = textos[textos.length-2].replace("(", "");
        monto = textos[textos.length-1];
        texto_monto_final.innerHTML = 'Monto Final ' + moneda;
    }else{
        texto_monto_final.innerHTML = 'Monto Final';
    }
    calcular($('#id_monto')[0]);
}

function calcular(monto) {
    if ($('#moneda')[0].innerHTML == $('#monto_final')[0].parentElement.children[0].innerHTML.split(' ')[2]) {
        monto_final.value = monto.value;
    } else if ($('#moneda')[0].innerHTML == '$') {
        monto_final.value = monto.value * $('#id_tipo_cambio')[0].value;
    } else {
        monto_final.value = monto.value / $('#id_tipo_cambio')[0].value;
    }
}

$('#id_ingresos').unbind().on('change', function (e) {
    seleccionar_ingresos(e.target);
})

$('#id_monto').unbind().on('input', function (e) {
    calcular(e.target);
})


monto_final = $('#monto_final')[0];
texto_monto = $('#id_monto')[0].parentElement.children[0];
texto_monto.innerHTML = 'Moneda ' + $('#moneda')[0].innerHTML;

seleccionar_ingresos($('#id_ingresos')[0])
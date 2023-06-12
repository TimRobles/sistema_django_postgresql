function seleccionar_nota(nota) {
    texto = getSelectedValueText(nota, nota.value);
    textos = texto.split(' ');
    monto = $('#id_monto')[0];
    texto_monto = monto.parentElement.children[0];
    if (textos.length > 1) {
        moneda = textos[textos.length-2].replace("(", "");
        monto = textos[textos.length-1];
        texto_monto.innerHTML = 'Monto ' + moneda;
    }else{
        texto_monto.innerHTML = 'Monto';
    }
    calcular($('#id_monto')[0]);
}

function calcular(monto) {
    if ($('#moneda')[0].innerHTML == $('#id_monto')[0].parentElement.children[0].innerHTML.split(' ')[1]) {
        monto_final.value = monto.value;
    } else if ($('#moneda')[0].innerHTML == '$') {
        monto_final.value = monto.value / $('#id_tipo_cambio')[0].value;
    } else {
        monto_final.value = monto.value * $('#id_tipo_cambio')[0].value;
    }
}

$('#id_nota').unbind().on('change', function (e) {
    seleccionar_nota(e.target);
})

$('#id_monto').unbind().on('input', function (e) {
    calcular(e.target);
})

$('#id_tipo_cambio').unbind().on('input', function (e) {
    calcular($('#id_monto')[0]);
})

monto_final = $('#monto_final')[0];
texto_monto_final = $('#monto_final')[0].parentElement.children[0];
texto_monto_final.innerHTML = 'Moneda Final ' + $('#moneda')[0].innerHTML;

seleccionar_nota($('#id_nota')[0])

function select_form() {
    console.log('Seleccionar')
    combos = document.getElementsByClassName('select2');
    for (let index = 0; index < combos.length; index++) {
        const element = combos[index];
        element.className = element.className.replace('select2-container--default select2-container--focus', 'form-control');
        element.className = element.className.replace('select2-container--default', 'form-control');
        element.className = element.className.replace('select2-container--focus', '');
        element.className = element.className.replace('select2-selection--single', '');
    }
}

setTimeout(() => {
    select_form();
}, 500);

select_form();
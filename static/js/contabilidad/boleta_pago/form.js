function calcular() {
    aporte_obligatorio = parseFloat($('#aporte_obligatorio')[0].innerHTML);
    comision_flujo_mixta = parseFloat($('#comision_flujo_mixta')[0].innerHTML);
    comision_flujo = parseFloat($('#comision_flujo')[0].innerHTML);
    prima_seguro = parseFloat($('#prima_seguro')[0].innerHTML);
    tipo_comision = parseFloat($('#tipo_comision')[0].innerHTML);
    rmv = parseFloat($('#rmv')[0].innerHTML);
    essalud = parseFloat($('#essalud')[0].innerHTML);
    movilidad = parseFloat($('#movilidad')[0].innerHTML);
    planilla = $('#planilla')[0].innerHTML;
    asignacion_familiar = $('#asignacion_familiar')[0].innerHTML;
    
    haber_mensual = parseFloat($('#id_haber_mensual')[0].value);
    if (asignacion_familiar == 'True') {
        asig_familiar = 0.1 * rmv;
    } else {
        asig_familiar = 0.00;
    }
    $('#id_asig_familiar')[0].value = asig_familiar;
    $('#id_movilidad')[0].value = movilidad;
    
    lic_con_goce_haber = parseFloat($('#id_lic_con_goce_haber')[0].value);
    dominical = parseFloat($('#id_dominical')[0].value);
    vacaciones = parseFloat($('#id_vacaciones')[0].value);
    compra_vacaciones = parseFloat($('#id_compra_vacaciones')[0].value);
    gratificacion = parseFloat($('#id_gratificacion')[0].value);
    ley29351 = parseFloat($('#id_ley29351')[0].value);
    cts = parseFloat($('#id_cts')[0].value);
    bonif_1mayo = parseFloat($('#id_bonif_1mayo')[0].value);
    
    aporte_obligatorio = Math.round(((haber_mensual + compra_vacaciones + asig_familiar + bonif_1mayo) * aporte_obligatorio)*100)/100;
    $('#id_aporte_obligatorio')[0].value = aporte_obligatorio;
    essalud = Math.round(((haber_mensual + compra_vacaciones + asig_familiar + bonif_1mayo) * essalud)*100)/100;
    $('#id_essalud')[0].value = essalud;
    if (tipo_comision == 1){
        comision = Math.round(((haber_mensual + compra_vacaciones + asig_familiar + bonif_1mayo) * comision_flujo_mixta)*100)/100;
    }else if (tipo_comision == 2){
        comision = Math.round(((haber_mensual + compra_vacaciones + asig_familiar + bonif_1mayo) * comision_flujo)*100)/100;
    }else{
        comision = 0.00;
    }
    $('#id_comision')[0].value = comision;
    prima_seguro =  Math.round(((haber_mensual + compra_vacaciones + asig_familiar + bonif_1mayo) * prima_seguro)*100)/100;
    $('#id_prima_seguro')[0].value = prima_seguro;
    
    impuesto_quinta = parseFloat($('#id_impuesto_quinta')[0].value);
    neto_recibido = Math.round(((haber_mensual + compra_vacaciones) + lic_con_goce_haber + dominical + movilidad + asig_familiar + vacaciones + gratificacion + ley29351 + cts + bonif_1mayo - aporte_obligatorio - comision - prima_seguro - impuesto_quinta)*100)/100;
    console.log(neto_recibido);
    $('#id_neto_recibido')[0].value = neto_recibido;

}

function calcular_total() {
    haber_mensual = parseFloat($('#id_haber_mensual')[0].value);
    asig_familiar = parseFloat($('#id_asig_familiar')[0].value);
    movilidad = parseFloat($('#id_movilidad')[0].value);
    lic_con_goce_haber = parseFloat($('#id_lic_con_goce_haber')[0].value);
    dominical = parseFloat($('#id_dominical')[0].value);
    vacaciones = parseFloat($('#id_vacaciones')[0].value);
    compra_vacaciones = parseFloat($('#id_compra_vacaciones')[0].value);
    gratificacion = parseFloat($('#id_gratificacion')[0].value);
    ley29351 = parseFloat($('#id_ley29351')[0].value);
    cts = parseFloat($('#id_cts')[0].value);
    bonif_1mayo = parseFloat($('#id_bonif_1mayo')[0].value);
    aporte_obligatorio = parseFloat($('#id_aporte_obligatorio')[0].value);
    comision = parseFloat($('#id_comision')[0].value);
    prima_seguro = parseFloat($('#id_prima_seguro')[0].value);
    impuesto_quinta = parseFloat($('#id_impuesto_quinta')[0].value);
    neto_recibido = Math.round(((haber_mensual + compra_vacaciones) + lic_con_goce_haber + dominical + movilidad + asig_familiar + vacaciones + gratificacion + ley29351 + cts + bonif_1mayo - aporte_obligatorio - comision - prima_seguro - impuesto_quinta)*100)/100;
    console.log(neto_recibido);
    $('#id_neto_recibido')[0].value = neto_recibido;

}

$('#calcular').on('click', calcular);

$('#id_impuesto_quinta').on('input', calcular_total);

$('#id_haber_mensual').on('input', calcular);
$('#id_compra_vacaciones').on('input', calcular);
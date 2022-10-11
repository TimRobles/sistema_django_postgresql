function elegir_direccion() {
    direccion = $('#id_direcciones')[0];
    direccion_partida = $('#id_direccion_partida')[0];
    direccion_destino = $('#id_direccion_destino')[0];
    ubigeo = $('#select2-id_ubigeo-container')[0];
    texto = getSelectedValueText(direccion, direccion.value);
    direccion_texto = texto.split(" | ")[0];
    ubigeo_texto = texto.split(" | ")[1];
    if (ubigeo_texto) {
        if (direccion_partida) {
            direccion_partida.value = direccion_texto;
        }
        if (direccion_destino) {
            direccion_destino.value = direccion_texto;
        }
        ubigeo.innerHTML = '---------';
    }
}

$('#id_direcciones').unbind().on('change', function () {
    elegir_direccion();
})
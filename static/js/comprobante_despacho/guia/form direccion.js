function elegir_direccion() {
    direccion = $('#id_direcciones')[0];
    direccion_destino = $('#id_direccion_destino')[0]
    ubigeo = $('#id_ubigeo')[0]
    ubigeo_container = $('.select2-container')[0]
    console.log(ubigeo_container);
    ubigeo_container.click();
    texto = getSelectedValueText(direccion, direccion.value);
    direccion_texto = texto.split(" | ")[0];
    ubigeo_texto = texto.split(" | ")[1];
    if (ubigeo_texto) {
        direccion_destino.value = direccion_texto;
        ubigeo.value = ubigeo_texto;
        console.log(ubigeo_texto);
    }
}

$('#id_direcciones').unbind().on('change', function () {
    elegir_direccion();
})
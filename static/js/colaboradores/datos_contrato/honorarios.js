function verificar_suspension_cuarta() {
    $suspension_cuarta = $('#id_suspension_cuarta')[0].checked;
    $archivo_suspension_cuarta = $('#id_archivo_suspension_cuarta')[0];

    if ($suspension_cuarta) {
        $archivo_suspension_cuarta.disabled = false;
    } else {
        $archivo_suspension_cuarta.value = null;
        $archivo_suspension_cuarta.disabled = true;
    }
}

$(document).on("change", "#id_suspension_cuarta", function () {
    verificar_suspension_cuarta();
});

verificar_suspension_cuarta();
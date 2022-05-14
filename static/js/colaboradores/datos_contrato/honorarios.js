function verificar_suspension_cuarta() {
    $suspension_cuarta = $('#id_suspension_cuarta')[0].checked;
    $year_suspension_cuarta = $('#id_year')[0];
    $archivo_suspension_cuarta = $('#id_archivo_suspension_cuarta')[0];

    if ($suspension_cuarta) {
        $year_suspension_cuarta.disabled = false;
        $archivo_suspension_cuarta.disabled = false;
    } else {
        $year_suspension_cuarta.value = null;
        $year_suspension_cuarta.disabled = true;
        $archivo_suspension_cuarta.value = null;
        $archivo_suspension_cuarta.disabled = true;
    }
}

$(document).on("change", "#id_suspension_cuarta", function () {
    verificar_suspension_cuarta();
});

verificar_suspension_cuarta();
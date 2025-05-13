function Dashboard() {
    console.log("Dashboard() called");
    usuario_id = $("#usuario_id").val();
    console.log(usuario_id);
    if (usuario_id == null || usuario_id == "") {
        usuario_id = 0;
    }
    usuario_nombre = $("#usuario_nombre").val();
    fecha_inicio = $("#fecha_inicio").val();
    fecha_fin = $("#fecha_fin").val();
    $("#usuario_seleccionado").text(usuario_nombre);
    url = "/dashboard_tabla/" + usuario_id + "/?fecha_inicio=" + fecha_inicio + "&fecha_fin=" + fecha_fin;
    console.log(url);
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            $("#dashboard").html($respuesta['table']);
        }else{
            $respuesta = false;
        }
    }
    xhr.send();
}

$("#usuarios").on("change", function() {
    $("#usuario_id").val($(this).val());
    $("#usuario_nombre").val($(this).find("option:selected").text());
    Dashboard();
});

$("#fecha_inicio").on("change", function() {
    Dashboard();
});

$("#fecha_fin").on("change", function() {
    Dashboard();
});
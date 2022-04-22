var asyncSuccessMessageCreate = [
    "<div ",
    "style='position:fixed;top:0;z-index:10000;width:100%;border-radius:0;' ",
    "class='alert alert-icon alert-success alert-dismissible fade show mb-0' role='alert'>",
    "Operación exitosa: Registro creado.",
    "<button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button>",
    "</div>",
    "<script>",
    "$('.alert').fadeTo(2000, 500).slideUp(500, function () {$('.alert').slideUp(500).remove();});",
    "<\/script>"
].join("");

var asyncSuccessMessageUpdate = [
    "<div ",
    "style='position:fixed;top:0;z-index:10000;width:100%;border-radius:0;' ",
    "class='alert alert-icon alert-success alert-dismissible fade show mb-0' role='alert'>",
    "Operación exitosa: Registro actualizado.",
    "<button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button>",
    "</div>",
    "<script>",
    "$('.alert').fadeTo(2000, 500).slideUp(500, function () {$('.alert').slideUp(500).remove();});",
    "<\/script>"
].join("");

var spinnerText = "<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>";
const spinnerDiv = document.createElement("div");
spinnerDiv.classList.add("form-control");
spinnerDiv.classList.add("btn");
spinnerDiv.classList.add("btn-info");
spinnerDiv.id = "spinnerDiv";
spinnerDiv.innerHTML = spinnerText;

var DentroModal = false;

function sleep (time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

function setSelectedValueText(selectObj, valueToSet) {
    for (var i = 0; i < selectObj.options.length; i++) {
        if (selectObj.options[i].text.toLowerCase() == valueToSet.toLowerCase()) {
            selectObj.options[i].selected = true;
            return;
        }
    }
}

function setSelectedValue(selectObj, valueToSet) {
    for (var i = 0; i < selectObj.options.length; i++) {
        if (selectObj.options[i].text== valueToSet) {
            selectObj.options[i].selected = true;
            return;
        }
    }
}

function setSelectedValueNext(selectObj, valueToSet) {
    for (var i = 0; i < selectObj.options.length; i++) {
        if (selectObj.options[i].text== valueToSet) {
            if (i + 1 == selectObj.options.length) {
                selectObj.options[0].selected = true;
            }else{
                selectObj.options[i+1].selected = true;
            }
            return;
        }
    }
}

$(function () {
    function createAsyncModalForm() {
        $(".create").each(function () {
            if ($(this).data("modal")) {
                modal="#modal-xl";
            }else{
                modal="#modal";
            };
            $(this).modalForm({
                formURL: $(this).data("form-url"),
                asyncUpdate: true,
                modalID:modal,
                asyncSettings: {
                    closeOnSubmit: true,
                    successMessage: asyncSuccessMessageCreate,
                    dataUrl: $(this).data("table-url"),
                    dataElementId: "#tabla",
                    dataKey: "table",
                    addModalFormFunction: reinstantiateModalForms
                }
            });
        });
    }
    createAsyncModalForm();

    // modal form
    function updateModalForm() {
        $(".update").each(function () {
            if ($(this).data("modal")) {
                modal="#modal-xl";
            }else{
                modal="#modal";
            };
            if ($(this).data("keep-open")) {
                close_submit=false;
            }else{
                close_submit=true;
            };
            $(this).modalForm({
                formURL: $(this).data("form-url"),
                asyncUpdate: true,
                modalID:modal,
                errorClass: ".invalid",
                asyncSettings: {
                    closeOnSubmit: close_submit,
                    successMessage: asyncSuccessMessageUpdate,
                    dataUrl: $(this).data("table-url"),
                    dataElementId: "#tabla",
                    dataKey: "table",
                    addModalFormFunction: reinstantiateModalForms
                }
            });
        });
    }
    updateModalForm();

    function formModalForm() {
        $(".form").each(function () {
            if ($(this).data("modal")) {
                modal="#modal-xl";
            }else{
                modal="#modal";
            };
            $(this).modalForm({
                formURL: $(this).data("form-url"),
                asyncUpdate: true,
                modalID:modal,
                asyncSettings: {
                    successMessage: asyncSuccessMessageUpdate,
                    dataUrl: $(this).data("table-url"),
                    dataElementId: "#tabla",
                    dataKey: "table",
                    addModalFormFunction: reinstantiateModalForms
                }
            });
        });
    }
    formModalForm();

    function deleteModalForm() {
        $(".delete").each(function () {
            $(this).modalForm({
                formURL: $(this).data("form-url"),
                isDeleteForm: true,
            });
        });
    }
    deleteModalForm();

    function readModalForm() {
        $(".read").each(function () {
            $(this).modalForm({
                formURL: $(this).data("form-url"),
                modalID: "#modal-xl-detail"
            });
        });
    }
    readModalForm();

    function reinstantiateModalForms() {
        createAsyncModalForm();
        readModalForm();
        updateModalForm();
        formModalForm();
        deleteModalForm();
        sleep(2000).then(function () {
            funcionesDentroModal()
        });
    }

    // Hide message
    $(".alert").fadeTo(2000, 500).slideUp(500, function () {
        $(".alert").slideUp(500);
    });

    $(document).on("click", "#consulta_ruc", function (e) {
        e.preventDefault();
        e.target.parentElement.appendChild(spinnerDiv);

        e.target.hidden = true;
        e.target.disabled = true;
        var ruc=$('#id_Ruc')[0].value;
        var razon_social=$('#id_RazonSocial');
        var url=$(this).data('url');
        consultaAjaxCallbackGet(url + ruc + '/', function(consulta){
            if (consulta) {
                info = JSON.parse(consulta['info'].replace(/&quot;/g,'"'));
                razon_social[0].value = info["razon_social"];
            }else{
                alert("Número no encontrado.");
            }
            spinnerDiv.remove();
            e.target.hidden = false;
            e.target.disabled = false;
        });
    }); 

    function spinner() {
        $(document).on("click", ".btn", function (e) {
            e.target.parentElement.parentElement.addEventListener("submit", function () {
                e.target.innerHTML = spinnerText;
                e.target.disabled = true;
            });
        });
    };

    function checkbox_div() {
        $(".form-check-input").wrap("<div class='input-group-text'></div>");
    };

    function funcionesDentroModal() {
        spinner();
        checkbox_div();
    }

    $('#modal').on('shown.bs.modal', function (e) {
        funcionesDentroModal();
    });

    $('#modal-xl').on('shown.bs.modal', function () {
        funcionesDentroModal();
    });
    
    
    function consultaAjaxCallback(datos, url, callback){
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.onload = function(){
            if (this.status === 200) {
                $respuesta = JSON.parse(xhr.responseText);
            }else{
                $respuesta = false;
            }
            callback($respuesta);
        }
        xhr.send(datos);
    };
    
    function consultaAjaxCallbackGet(url, callback){
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.onload = function(){
            if (this.status === 200) {
                $respuesta = JSON.parse(xhr.responseText);
            }else{
                $respuesta = false;
            }
            callback($respuesta);
        }
        xhr.send();
    };
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

/* Popover */
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
});
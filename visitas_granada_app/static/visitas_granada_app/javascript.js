$(document).ready(function(){ 
    // Lanza confirmación hasta de enviar la petición de borrado de una visita
    // Se añade al evento click de los botones de borrado.
    $(".delVisitaButton").click(function(){ 
        const del = confirm("¿Seguro que desea eliminar completamente la visita?");
        if (del == true) {
            window.location.href = '/visita_borrar/' + $(this).data("id");
        } 
    }); 
}); 
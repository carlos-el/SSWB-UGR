$(document).ready(function(){ 

    // Ejecutar este código cuando la página este caragada para poner el modo correcto
    // TODO es posible colocar esto al inicio del head?
    const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;
    if(currentTheme) {
        $(document.documentElement).attr("data-theme", currentTheme);
    
        if (currentTheme === 'dark') {
            $("#theme-switcher-moon").css("display", "none")
            $("#theme-switcher-sun").css("display", "inline-block")
        }
    }

    // Lanza confirmación hasta de enviar la petición de borrado de una visita
    // Se añade al evento click de los botones de borrado.
    $(".delVisitaButton").click(function(){ 
        const del = confirm("¿Seguro que desea eliminar completamente la visita?");
        if (del == true) {
            window.location.href = '/visita_borrar/' + $(this).data("id");
        } 
    }); 


    // Funcion para alternar entre el modo ocuro y el claro
    $("#theme-switcher-moon, #theme-switcher-sun").click(function(){ 
        if($(document.documentElement).attr("data-theme") == "dark"){
            $("#theme-switcher-moon").css("display", "inline-block")
            $("#theme-switcher-sun").css("display", "none")
            localStorage.setItem('theme', 'light');
            $(document.documentElement).attr("data-theme", "light");
        }else{
            $("#theme-switcher-moon").css("display", "none")
            $("#theme-switcher-sun").css("display", "inline-block")
            localStorage.setItem('theme', 'dark');
            $(document.documentElement).attr("data-theme", "dark");
        }

    }); 


}); 
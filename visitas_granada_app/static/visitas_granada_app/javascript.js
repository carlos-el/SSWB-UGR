$(document).ready(function () {

    // Ejecutar este código cuando la página este caragada para poner el modo correcto
    // TODO es posible colocar esto al inicio del head?
    const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;
    if (currentTheme) {
        $(document.documentElement).attr("data-theme", currentTheme);

        if (currentTheme === 'dark') {
            $("#theme-switcher-moon").css("display", "none")
            $("#theme-switcher-sun").css("display", "inline-block")
        }
    }

    // Funcion para alternar entre el modo ocuro y el claro
    $("#theme-switcher-moon, #theme-switcher-sun").click(function () {
        if ($(document.documentElement).attr("data-theme") == "dark") {
            $("#theme-switcher-moon").css("display", "inline-block")
            $("#theme-switcher-sun").css("display", "none")
            localStorage.setItem('theme', 'light');
            $(document.documentElement).attr("data-theme", "light");
        } else {
            $("#theme-switcher-moon").css("display", "none")
            $("#theme-switcher-sun").css("display", "inline-block")
            localStorage.setItem('theme', 'dark');
            $(document.documentElement).attr("data-theme", "dark");
        }

    });


    // Lanza confirmación hasta de enviar la petición de borrado de una visita
    // Se añade al evento click de los botones de borrado.
    $(".delVisitaButton").click(function () {
        const del = confirm("¿Seguro que desea eliminar completamente la visita?");
        if (del == true) {
            window.location.href = '/visita_borrar/' + $(this).data("id");
        }
    });

    // Funcion para enviar likes y dislikes a la REST API junto con la asignacion a los botones
    function sendLikesValue(value) {
        value = value.toString()
        $.ajax({
            url: location.origin + '/api/visitas/likes/' + location.pathname.split("/")[2] + "/",
            type: 'PUT',
            dataType: 'json',
            traditional: true,
            data: { 'likes': value },

            success: function (data) {
                $("#likes-value-holder").text(data.likes)
            }
        })
    }
    $("#like-btn").click(function () {
        const value = parseInt($("#likes-value-holder").text())
        sendLikesValue(value + 1)
    });
    $("#dislike-btn").click(function () {
        const value = parseInt($("#likes-value-holder").text())
        sendLikesValue(value - 1)
    });

    // Codigo para los mapas de OpenLayers
    // Obtener coordenadas de la visita
    const lat = $("#map").attr("lat")
    const lon = $("#map").attr("lon")
    const userLat = 0
    const userLon = 0
    let markers = []

        // Marcador de la visita
        markerVisita = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat])),
            name: 'Visita',
        })
        markerVisita.setStyle(new ol.style.Style({
            image: new ol.style.Icon(({
                anchor: [0.5, 1],
                src: "https://cdn.mapmarker.io/api/v1/font-awesome/v4/pin?icon=fa-star&size=30&hoffset=0&voffset=-1"
            })),
            text: new ol.style.Text({
                text: 'Visita',
                font: '14px Calibri,sans-serif',
                fill: new ol.style.Fill({ color: '#000' }),
                stroke: new ol.style.Stroke({
                    color: '#fff', width: 3
                })
            })
        })
        )
        // Añadimos el marcador
        markers.push(markerVisita)

    let map = new ol.Map({
        target: 'map',
        layers: [
            // Capa para obtener el mapa
            new ol.layer.Tile({
                source: new ol.source.OSM()
            }),
            // Capa para colocar marcador en el lugar de la visita y del usuario
            new ol.layer.Vector({
                source: new ol.source.Vector({
                    features: markers
                })
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([lon, lat]),
            zoom: 13
        })
    });
}); 
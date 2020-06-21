import React, { Component } from 'react'
import Comentario from "./detalleComentario"

import View from 'ol/View';
import Map from 'ol/Map';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';

import * as olStyle from 'ol/style';
import Tile from 'ol/layer/Tile';
import Vector from 'ol/layer/Vector';
import OSM from 'ol/source/OSM';
import VectorS from 'ol/source/Vector';
import * as olProj from 'ol/proj';

class Detalle extends Component {
    constructor(props) {
        super(props)

        // Inicializamos estado
        this.state = {
            visita: {},
            comentarios: [],
            likes: 0,
            map: null,
            id: this.props.match.params.id // Inicializamos el id al parametro de react router
        };

        // Bindeamos estas funciones para que se pueda 'this.state' dentro de ellas
        this.giveLike = this.giveLike.bind(this);
        this.giveDislike = this.giveDislike.bind(this);
    }

    componentDidMount() {
        // Código que permite que se vean los iconos de 'feather'
        const feather = require('feather-icons')
        feather.replace()

        // Pedimos las visitas y los comentarios cuando el componente se monta
        this.fetchVisita()
        this.fetchComentarios()
    }

    // Función para crear el mapa de Openlayers
    createMap(lati, long) {
        document.getElementById("map").innerHTML = "";
        // Codigo para los mapas de OpenLayers
        // Obtener coordenadas de la visita
        const lat = lati
        const lon = long
        let markers = []

        // Marcador de la visita
        let markerVisita = new Feature({
            geometry: new Point(olProj.fromLonLat([lon, lat])),
            name: 'Visita',
        })
        markerVisita.setStyle(new olStyle.Style({
            image: new olStyle.Icon(({
                anchor: [0.5, 1],
                src: "https://cdn.mapmarker.io/api/v1/font-awesome/v4/pin?icon=fa-star&size=30&hoffset=0&voffset=-1"
            })),
            text: new olStyle.Text({
                text: 'Visita',
                font: '14px Calibri,sans-serif',
                fill: new olStyle.Fill({ color: '#000' }),
                stroke: new olStyle.Stroke({
                    color: '#fff', width: 3
                })
            })
        })
        )
        // Añadimos el marcador
        markers.push(markerVisita)

        let map = new Map({
            target: 'map',
            layers: [
                // Capa para obtener el mapa
                new Tile({
                    source: new OSM()
                }),
                // Capa para colocar marcador en el lugar de la visita y del usuario
                new Vector({
                    source: new VectorS({
                        features: markers
                    })
                })
            ],
            view: new View({
                center: olProj.fromLonLat([lon, lat]),
                zoom: 13
            })
        });

        return map;
    }

    // Función para pedir la info de la visita a la API REST
    fetchVisita() {
        fetch("http://localhost:80/api/visitas/" + this.state.id, {
            method: "GET",
            headers: {
                'Accept': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if("error" in data){
                    alert(data.error);
                } else { 
                    this.setState({ visita: data, likes: data.likes })
                    // Al tener los datos de la visita podemos crear el mapa correctamente
                    let map = this.createMap(data.lat, data.lon)
                    // Reescalamos el mapa para que se ajuste a las medidas de su contenedor
                    setTimeout(() => {
                        map.updateSize();
                    }, 200);
                }
            }
            ).catch(err => {
                alert("Error inesperado, intentelo más tarde.");
            });
    }

    // Función para pedir la info de los comentarios a la API REST
    fetchComentarios() {
        fetch("http://localhost:80/api/visitas/comentarios/" + this.state.id, {
            method: "GET",
            headers: {
                'Accept': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if("error" in data){
                    alert(data.error);
                } else { 
                    this.setState({ comentarios: data.comentarios})
                }
            }
            ).catch(err => {
                alert("Hubo un error al intentar mostrar los comentarios, intentelo maś tarde.");
            });
    }

    // Función para dar 'like' a la visita
    giveLike() {
        var urlencoded = new URLSearchParams();
        urlencoded.append("likes", (this.state.likes + 1).toString());

        fetch("http://localhost:80/api/visitas/likes/" + this.state.id + "/", {
            method: "PUT",
            headers: {
                'Accept': 'application/json',
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: urlencoded
        })
            .then(response => response.json())
            .then(data => {
                if("error" in data){
                    alert(data.error);
                } else { 
                    this.setState({ likes: data.likes })
                }
            }
            ).catch(err => {
                alert("Hubo un error al realizar esta acción, intentelo maś tarde.");
            });
    }

    // Función para dar 'dislike' a la visita
    giveDislike() {
        var urlencoded = new URLSearchParams();
        urlencoded.append("likes", (this.state.likes - 1).toString());

        fetch("http://localhost:80/api/visitas/likes/" + this.state.id + "/", {
            method: "PUT",
            headers: {
                'Accept': 'application/json',
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: urlencoded
        })
            .then(response => response.json())
            .then(data => {
                if("error" in data){
                    alert(data.error);
                } else { 
                    this.setState({ likes: data.likes })
                }
            }
            ).catch(err => {
                alert("Hubo un error al realizar esta acción, intentelo maś tarde.");
            });
    }

    render() {
        return (
            <React.Fragment>
                <div className="container-fluid mt-2 mt-sm-5">
                    <div className="row px-4">
                        <div className="col-xs-6 col-sm-5 col-md-4 col-lg-3">
                            <img src={"http://localhost:80" + this.state.visita.foto} className="w-100" alt="..."></img>
                            <p className="h5 text-center mt-3"><b id="likes-value-holder">{this.state.likes}</b> Me gusta <i className="feather-24"
                                data-feather="heart"></i></p>
                            <p className="text-center"><span id="like-btn" onClick={this.giveLike}><i className="feather-24 scale-on-hover" data-feather="thumbs-up"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;<span id="dislike-btn" onClick={this.giveDislike}><i className="feather-24 scale-on-hover" data-feather="thumbs-down"></i></span></p>
                        </div>
                        <div className="col-xs-6 col-sm-7 col-md-8 col-lg-6  mt-3 mt-sm-0">
                            <h3 className="mb-3 text-center text-sm-left" style={{ fontWeight: "bold" }}>{this.state.visita.nombre}</h3>
                            <p>{this.state.visita.descripcion}</p>
                        </div>
                        <div className="map col-lg-3  mt-3 mt-sm-0" id="map" lat={this.state.visita.lat} lon={this.state.visita.lon}></div>
                    </div>
                </div>

                <div className="row mt-3">
                    <div className="col">
                        <hr/>
                    </div>
                    <div className="col-auto">
                        <h4>Comentarios:</h4>
                    </div>
                    <div className="col">
                        <hr/>
                    </div>
                </div>

                <div className="row p-4">
                    <div className="col-12">
                        { this.state.comentarios.map((comentario, index) => {
                            return(
                                    <Comentario key={index} texto={comentario.texto}/>
                            );
                        })}
                        { (this.state.comentarios.length === 0) ? <b>No hay comentarios en esta visita.</b> : "" }
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

export default Detalle;
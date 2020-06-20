import React, { Component } from 'react'
import ColumnaFiltros from './listadoColumnaFiltros';
import CartaVisita from './listadoCartaVisita';

class Listado extends Component{
    constructor(props){
        super(props)

        this.state = {
            visitas: []
        };
    }

    componentDidMount(){
        // Cuando el componente este montado pedimos las visitas a la API
        this.fetchVisitas()
    }

    // Función para pedir las visitas a la API REST
    fetchVisitas(){
        fetch("http://localhost:8000/api/visitas/", {
            method: "GET",
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            this.setState({visitas: data.visitas})       
        }
        ).catch(err => {
            alert("Error inesperado del servidor, por favor, intentelo maś tarde.");
        });
    }

    render() {
        return (
            <React.Fragment>
                {/* Carrousel con titulo */}
                <div className="container-fluid m-0 p-0">
                    <div className="row m-0 p-0">
                        <div className="col px-0">
                            <div id="carouselListaVisitas" className="carousel slide position-relative" data-ride="carousel">
                                <div className="carousel-inner">
                                    <div className="carousel-item active" data-interval="5000">
                                        <img src="http://localhost:8000/media/fotos/granada.jpg" className="d-block w-100" alt="..."></img>
                                    </div>
                                    <div className="carousel-item" data-interval="5000">
                                        <img src="http://localhost:8000/media/fotos/granada2.jpg" className="d-block w-100" alt="..."></img>
                                    </div>
                                </div>
                            </div>

                            <div className="titleListaVisitas container-fluid pl-0">
                                <h3 className="title text-center">Visitas en Granada</h3>
                                <p className="titleCaption text-center">¡Hay mucho por descubrir!</p>
                            </div>

                        </div>
                    </div>
                </div>

                {/* Página principal */}
                <div className="container-fluid px-3 pt-2 px-xl-5 pt-md-4">
                    <div className="row">
                        {/* Columna filtros */}
                        <ColumnaFiltros />
                        {/* Columna cartas */}
                        <div className="cardsCol col-md-8 col-xl-9 mb-4">
                            <div className="row">  
                                { this.state.visitas.map((visita) => {
                                    return(
                                        <div key={visita.id} className="col-12 col-xl-6">
                                            <CartaVisita visita={visita}/>
                                        </div>
                                    );
                                })}
                                { (this.state.visitas.length === 0) ? <p className="text-danger">No hay visitas registradas en el sistema.</p> : "" }
                            </div>   
                        </div>
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

export default Listado;
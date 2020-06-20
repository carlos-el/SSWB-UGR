import React, { Component } from 'react'
import { Link } from "react-router-dom";

// Componenete que renderiza la 'card' de una visita en el listado de visitas
class CartaVisita extends Component{
    render() {
        // Reducimos la descripción si es muy larga para que quepa en la 'card'.
        let visita = this.props.visita
        if (visita.descripcion.length > 100)
            visita.descripcion = visita.descripcion.slice(0,97) + "..."

        return (
            <Link to={"/visitas/" + visita.id}>
                <div className="card p-3 mt-3 border-0 shadow" style={{maxWidth: "760px"}}>
                    <div className="row no-gutters">
                        <div className="col-md-4 align-self-center">
                            <img src={"http://localhost:8000" + visita.foto} className="card-img"
                                style={{maxWidth: "180px", maxHeight: "180px", height: "auto"}} alt="..."></img>
                        </div>
                        <div className="col-md-8">
                            <div className="card-body py-0 px-0 pt-3 pt-md-0 pl-md-3">
                                <h5 className="card-title text-primary" style={{fontWeight: "bold"}}>{ visita.nombre }</h5>
                                <p className="card-text text-dark">
                                        { visita.descripcion }
                                </p>
                                <p className="card-text"><small className="text-muted">Esta visita ha gustado a&nbsp;
                                        { visita.likes } personas.</small></p>
                            </div>
                        </div>
                    </div>
                </div>
            </Link>
        );
    }
}

export default CartaVisita;
import React, { Component } from 'react'

// Componente que renderiza el texto de un comentario
class Comentario extends Component {

    render() {
        return (
            <React.Fragment >
                <p>{ this.props.texto }</p>
                <div>
                    <hr/>
                </div>
            </React.Fragment>
        );
    }
}

export default Comentario;
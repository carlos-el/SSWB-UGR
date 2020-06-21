import React, { Component } from 'react'
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
} from "react-router-dom";
import $ from "jquery";

import Listado from "./listado"
import Detalle from "./detalle"

class Base extends Component {

    componentDidMount() {
        // Código que permite que se vean los iconos de 'feather'
        const feather = require('feather-icons')
        feather.replace()

        // Ejecutar este código cuando la página este caragada para poner el modo de iluminación correcto
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
            if ($(document.documentElement).attr("data-theme") === "dark") {
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
    }

    render() {
        return (
            <React.Fragment>
                <Router>
                    <header>
                        <nav className="navbar navbar-expand-lg navbar-light bg-primary">
                            <Link to="/">
                                <span className="navbar-brand">
                                    <img src="http://localhost:80/media/fotos/default.png" width="30" height="30" alt="" />
                                </span>
                            </Link>
                            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                                <span className="navbar-toggler-icon"></span>
                            </button>

                            <div className="collapse navbar-collapse ml-3 mr-3" id="navbarSupportedContent">
                                <ul className="navbar-nav mr-auto">
                                    <li className="nav-item">
                                        <Link to="/visitas">
                                            <span className="nav-link active" >Inicio<span className="sr-only">(current)</span></span>
                                        </Link>
                                    </li>
                                    <li className="nav-item dropdown">
                                        <a className="nav-link active dropdown-toggle" href="/#" id="navbarDropdown" role="button" data-toggle="dropdown"
                                            aria-haspopup="true" aria-expanded="false">
                                            Desplegable
                                        </a>
                                        <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                            <a className="dropdown-item" href="/#">Acción</a>
                                            <a className="dropdown-item" href="/#">Otra acción</a>
                                            <div className="dropdown-divider"></div>
                                            <a className="dropdown-item" href="/#">Algo más aquí</a>
                                        </div>
                                    </li>
                                </ul>
                                <ul className="navbar-nav ml-md-auto">
                                    <li className="nav-item dropdown">
                                        <a className="nav-item nav-link active dropdown-toggle mr-md-2" href="/#" id="bd-versions" data-toggle="dropdown"
                                            aria-haspopup="true" aria-expanded="false">
                                            Idioma
                                        </a>
                                        <div className="dropdown-menu dropdown-menu-md-right" aria-labelledby="bd-versions">
                                            <a className="dropdown-item active" href="/#">Idioma 1</a>
                                            <div className="dropdown-divider" href="/#"></div>
                                            <a className="dropdown-item active" href="/#">Idioma 2</a>
                                            <div className="dropdown-divider" href="/#"></div>
                                            <a className="dropdown-item active" href="/#">Idioma 3</a>
                                        </div>
                                    </li>
                                    <li className="nav-item mr-2">
                                        <span className="nav-link active" href="/#"><i id="theme-switcher-moon" className="feather-20" data-feather="moon"></i><i
                                            id="theme-switcher-sun" className="feather-20 not-display" data-feather="sun"></i></span>
                                    </li>
                                </ul>
                                <form className="form-inline my-2 my-lg-0">
                                    <input className="form-control mr-sm-2" type="search" placeholder="Búsqueda" aria-label="Search"></input>
                                    <button className="btn btn-outline-dark bg-dark text-light my-2 my-sm-0" type="submit"><b>Buscar</b></button>
                                </form>
                            </div>
                        </nav>
                    </header>

                    {/* Switchs de React Router que permiten cambiar el componente renderizado en esta posición según la URL pedida. */}
                    {/* El orden es relevante. */}
                    <Switch>
                        <Route path="/visitas/:id" component={Detalle} />
                        <Route path="/visitas"> <Listado /> </Route>
                        <Route path="/"> <Listado /> </Route>
                    </Switch>

                </Router>
            </React.Fragment>
        );
    }
}

export default Base;
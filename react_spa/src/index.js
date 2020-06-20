import React from 'react';
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import Base from "./components/base"

//JS imports
import 'popper.js/dist/popper.min.js'
import 'bootstrap/dist/js/bootstrap.min.js'

//CSS imports
import 'bootstrap/dist/css/bootstrap.css'
import './index.css';
import 'ol/ol.css';

// Renderizar el componente principal de la SPA
ReactDOM.render(
  <React.StrictMode>
    <Base />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

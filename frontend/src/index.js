import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter} from "react-router-dom";
import withReduxFeatures from './withReduxFeatures';
import App from './components/App';
import './index.css';
import * as serviceWorker from './serviceWorker';
import 'bootstrap/dist/css/bootstrap.min.css';
import './i18n';
import "leaflet/dist/leaflet.css";

/** Wrap App component with store providers */
const WrappedApp = withReduxFeatures(App);

ReactDOM.render(
    <BrowserRouter>
    
    <WrappedApp />
    </BrowserRouter>,
     document.getElementById('root'));

/**
 * If you want your app to work offline and load faster,
 * you can change unregister() to register() below.
 * Note this comes with some pitfalls.
 * @see https://bit.ly/CRA-PWA
 */
serviceWorker.unregister();

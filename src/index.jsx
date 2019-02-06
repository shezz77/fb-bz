import React from 'react';
import ReactDOM from 'react-dom';
import App from './app';

if (document.getElementById('app')) {
    ReactDOM.render(
        <App />,
    document.getElementById('app'));
}

const express = require('express');
const app = express();
const path = require('path');

//middleware to handle json
app.use(express.json());

// middleware to handle urlencoded form data
app.use(
    express.urlencoded({
        extended: false,
    })
);

// serve static file
app.use('/', express.static(path.join(__dirname, '/public')));

// default route
app.use('/', require('./routes/root'));

// api routes
app.use('/api', require('./routes/api/api'));

module.exports = app;

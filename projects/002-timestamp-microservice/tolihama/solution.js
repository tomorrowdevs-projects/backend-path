// Dependencies
const express = require("express"); 
const bodyParser = require('body-parser');

// Custom dependencies

// Express App config
const app = express(); 
const PORT = process.env.PORT || 3000; 

// API Route timestamp microservice
// No params: current time
app.get('/api', (req, res) => {
    const now = new Date();

    res.status(200).send({
        unix: now.getTime(),
        utc: now.toUTCString(),
    });
});

// Date param
app.get('/api/:date', (req, res) => {
    const date = req.params.date;

    res.status(200).send({ date });
});

// Run server
app.listen(PORT, () => { 
    console.log(`API is listening on port ${PORT}`); 
});
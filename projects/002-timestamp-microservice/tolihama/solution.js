// Dependencies
const express = require("express"); 

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
    const dateParam = /[^0-9]/g.test(req.params.date)
                        ? req.params.date 
                        : parseInt(req.params.date);
    const date = new Date(dateParam);

    if(isNaN(date)) {
        res.status(200).send({ error: 'Invalid Date' });
        return;
    }

    res.status(200).send({
        unix: date.getTime(),
        utc: date.toUTCString(),
    });
});

// Run server
app.listen(PORT, () => { 
    console.log(`API is listening on port ${PORT}`); 
});
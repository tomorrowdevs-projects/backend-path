// Dependencies
const express = require("express"); 

// Express App config
const app = express(); 
const PORT = process.env.PORT || 3000; 

// Header Parser Route
app.get('/api/whoami', (req, res) => {
    res.status(200).send({ 
        ip: req.ip,
        language: req.get('Accept-Language'),
        software: req.header('User-Agent'),
    });
});

// Run server
app.listen(PORT, () => { 
    console.log(`API is listening on port ${PORT}`); 
});
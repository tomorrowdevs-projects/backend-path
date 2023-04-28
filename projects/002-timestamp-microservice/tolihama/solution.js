// Dependencies
const express = require("express"); 
const bodyParser = require('body-parser');

// Custom dependencies

// Express App config
const app = express(); 
const PORT = process.env.PORT || 3000; 


// Run server
app.listen(PORT, () => { 
    console.log(`API is listening on port ${PORT}`); 
});
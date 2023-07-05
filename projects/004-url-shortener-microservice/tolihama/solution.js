// Dependencies
const express = require("express"); 
const bodyParser = require('body-parser');
const routes = require("./routes/url_shortener");

// Express App config
const app = express(); 
const PORT = process.env.PORT || 3000; 

// Configuring body parser middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Use routes from routes files
app.use('/', routes);

// Run server
app.listen(PORT, () => { 
    console.log(`API is listening on port ${PORT}`); 
});
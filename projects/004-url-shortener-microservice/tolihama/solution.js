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

// Calculator APIs
// Create New Shortened Url Route
/*app.post("/api/shorturl", (req, res) => {
    const reqBody = req.body;

    // Check if exist 'original_url' key in body request
    if(!reqBody.hasOwnProperty('original_url')) {
        res.status(400).send({
            error: "Missing 'original_url' key in body request.",
        });
        return;
    }

    const originalUrl = reqBody.original_url;
    // Check if 'original_url' is a string with the correct format
    if(isValidUrl(originalUrl)) {
        res.status(400).send({
            error: "invalid url",
        });
        return;
    }

    // If request is validated, add 'original_url' in shortenedUrlsList
    shortenedUrlsList.push(originalUrl);

    console.log(shortenedUrlsList)

    res.status(200).send({
        original_url: originalUrl,
        short_url: shortenedUrlsList.length,
    });
});*/


// Run server
app.listen(PORT, () => { 
    console.log(`API is listening on port ${PORT}`); 
});

/*const isValidUrl = urlString => {
    try { 
        return Boolean(new URL(urlString)); 
    }
    catch(e){ 
        return false; 
    }
}*/
// Dependencies
const express = require("express"); 
const bodyParser = require('body-parser');

// Express App config
const app = express(); 
const PORT = process.env.PORT || 3000; 

// Configuring body parser middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// For testing purposes 
app.get("/", (req, res) => { 
    res.send("<h2>It's Working!</h2>"); 
}); 


// Calculator APIs
app.post("/sum", (req, res) => {
    const reqBody = req.body;

    // Verify Requested Params in Body Request
    if(!reqBody.hasOwnProperty('addendOne')) res.status(400).send({ 'error_message': 'Missing \'addendOne\' key in body request' });
    if(!reqBody.hasOwnProperty('addendTwo')) res.status(400).send({ 'error_message': 'Missing \'addendTwo\' key in body request' });

    const addendOne = parseFloat(reqBody.addendOne);
    const addendTwo = parseFloat(reqBody.addendTwo);

    // Verify Params are numbers
    if(isNaN(addendOne)) res.status(400).send({ 'error_message': '\'addendOne\' is not a number'});
    if(isNaN(addendTwo)) res.status(400).send({ 'error_message': '\'addendTwo\' is not a number'});

    res.status(200).send({
        'result': addendOne + addendTwo,
    });
});

app.post("/subtraction", (req, res) => {
    const reqBody = req.body;
});

app.post("/multiply", (req, res) => {
    const reqBody = req.body;
});

app.post("/division", (req, res) => {
    const reqBody = req.body;
});



// Run server
app.listen(PORT, () => { 
    console.log(`API is listening on port ${PORT}`); 
});
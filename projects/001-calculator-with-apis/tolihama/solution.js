// Dependencies
const express = require("express"); 
const bodyParser = require('body-parser');
const validator = require('./validatorClass');

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

    const errors = validator.validate(reqBody, {
        'addendOne': 'requested|number',
        'addendTwo': 'requested|number',
    });

    if(errors) {
        res.status(400).send({errors});
        return;
    }

    res.status(200).send({
        'result': req.body.addendOne + req.body.addendTwo,
    });
});

app.post("/subtraction", (req, res) => {
    const reqBody = req.body;

    const errors = validator.validate(reqBody, {
        'minuend': 'requested|number',
        'subtrahend': 'requested|number',
    });

    if(errors) {
        res.status(400).send({errors});
        return;
    }

    res.status(200).send({
        'result': req.body.minuend - req.body.subtrahend,
    });
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
// Dependencies
const express = require("express"); 
const bodyParser = require('body-parser');

// Custom dependencies
const validator = require('./validatorClass');

// Express App config
const app = express(); 
const PORT = process.env.PORT || 3000; 

// Configuring body parser middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// SWAGGER docs
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const swaggerDocument = YAML.load('./swagger.yaml');
app.use(
    '/api-docs',
    swaggerUi.serve, 
    swaggerUi.setup(swaggerDocument)
);

// Calculator APIs
app.post("/sum", (req, res) => {
    const reqBody = req.body;s

    const errors = validator.validate(reqBody, {
        'addendOne': 'requested|number',
        'addendTwo': 'requested|number',
    });

    if(errors) {
        res.status(400).send({errors});
        return;
    }

    res.status(200).send({
        'result': parseFloat(req.body.addendOne) + parseFloat(req.body.addendTwo),
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
        'result': parseFloat(req.body.minuend) - parseFloat(req.body.subtrahend),
    });
});

app.post("/multiply", (req, res) => {
    const reqBody = req.body;

    const errors = validator.validate(reqBody, {
        'multiplier': 'requested|number',
        'multiplicand': 'requested|number',
    });

    if(errors) {
        res.status(400).send({errors});
        return;
    }

    res.status(200).send({
        'result': parseFloat(req.body.multiplier) * parseFloat(req.body.multiplicand),
    });
});

app.post("/division", (req, res) => {
    const reqBody = req.body;

    const errors = validator.validate(reqBody, {
        'dividend': 'requested|number',
        'divisor': 'requested|number',
    });

    if(errors) {
        res.status(400).send({errors});
        return;
    }

    res.status(200).send({
        'result': parseFloat(req.body.dividend) / parseFloat(req.body.divisor),
    });
});

// Run server
app.listen(PORT, () => { 
    console.log(`API is listening on port ${PORT}`); 
});
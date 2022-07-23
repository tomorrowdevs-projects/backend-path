const env = require('dotenv').config();
const express = require('express');
const app = express();
const port = process.env.PORT;
const connectDB = require('./config/dbConn');
const mongoose = require('mongoose');
const path = require('path');

//Connect to mongoDB
connectDB();

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

mongoose.connection.once('open', () => {
    console.log('Connected to the DB');
    app.listen(port, () => {
        console.log(`Exercise tracker app listening on port ${port}!`);
    });
});

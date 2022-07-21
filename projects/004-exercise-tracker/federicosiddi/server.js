const env = require('dotenv').config();
const express = require('express');
const app = express();
const port = process.env.PORT;
const connectDB = require('./config/dbConn');
const mongoose = require('mongoose');

//Connect to mongoDB
connectDB();

app.use(express.json());
app.use(
    express.urlencoded({
        extended: false,
    })
);
app.use('/api', require('./routes/api'));

app.get('/', (req, res) => res.send('Welcome to the exercise tracker API!'));

mongoose.connection.once('open', () => {
    console.log('Connected to the DB');
    app.listen(port, () => {
        console.log(`Exercise tracker app listening on port ${port}!`);
    });
});

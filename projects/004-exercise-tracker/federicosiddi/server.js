const env = require('dotenv').config();
const connectDB = require('./config/dbConn');
const mongoose = require('mongoose');
const PORT = process.env.PORT;
const app = require('./app');

//Connect to mongoDB
connectDB();

mongoose.connection.once('open', () => {
    console.log('Connected to the DB');
    app.listen(PORT, () => {
        console.log(`Exercise tracker app listening on port ${PORT}!`);
    });
});

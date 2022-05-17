const express: any = require('express');

const app = express();

// app use will set a "prefix", whem the get call have /api it will be redirect on the roots in require file
app.use('/api', require('./api/date/apidate'))

app.listen(3000, () => {
    console.log('server ready')
});
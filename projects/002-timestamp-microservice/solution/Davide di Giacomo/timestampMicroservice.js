//A request to /api/:date? with a valid date should return a JSON object 
//with a unix key that is a Unix timestamp of the input date in milliseconds

const express = require('express')
const app = express()

app.get('/api/:date?', (req, res) => {
    const { date } = req.params

    //verify if the date is correct
    if (Number.isInteger(Number(date)) === true) {

        let d = new Date(Number(date));
        let milliseconds = d.getTime();

        res.status(200).json({unix: milliseconds, utc: d});

    }else if (date === undefined) {
        let d = new Date();
        let milliseconds = d.getTime();

        res.status(200).json({unix: milliseconds, utc: d});
    }
    else {
        res.status(200).json({error: "Invalid Date"});
    }
    
})


app.listen(3000)
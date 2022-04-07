const express = require('express')
const app = express()
const port = 3000


// a request at /api/date? with unix date will return a json with date converted to utc standard
// a request at /api/date? with utc date will return a json with date converted to unix standard
app.get('/api/:date?', (req, res) => {
    try {
        stringDate = req.params.date
        // if there are spaces in the date parameters it tries to
        // convert the utc date to unix
        if (stringDate.includes(" ") || stringDate.includes("-") || stringDate.includes(":")) {
            console.log("Entered")
            // if date parsing to unix returns null it sends error obj
            parsedDate = Date.parse(stringDate)
            if (isNaN(new Date(stringDate).getTime() / 1000)) {
                throw err
            } else {
                parsedDate = Date.parse(stringDate)
                utcDate = new Date(stringDate).toUTCString()
                unixDate = parsedDate
                resObj = {
                    "unix": unixDate,
                    "utc": utcDate
                }
                res.json(resObj)
            }
            // if we arrive here it means that we have a unix timestamp string
        } else {
            // here we convert timestamp string to int
            unixDate = parseInt(inputDate)
            // if converting the timestamp results in an Invalid Date we throw an error
            if (new Date(unixDate).toUTCString() === "Invalid Date") {
                throw err
            } else {
                utcDate = new Date(unixDate).toUTCString()
                resObj = {
                    "unix": unixDate,
                    "utc": utcDate
                }
                res.json(resObj)
            }
        }
    } catch (err) {
        // if the date string is invalid the api returns a json with an error msg
        res.json({
            error: "Invalid Date"
        })
    }

})

// the /api/ route without parameters will return current time in unix and utc 
app.get('/api/', (req, res) => {
    res.json({
        "unix": Date.now(),
        "utc": new Date().toUTCString()
    })

})

//  home route will send hello world message
app.get('/', (req, res) => res.send('Hello World!'))


app.listen(port, () => console.log(`Example app listening on port ${port}!`))
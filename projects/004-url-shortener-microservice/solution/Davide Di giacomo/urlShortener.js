const express = require('express')
const app = express()
const {url} = require("./url")


//POST a URL to /api/shorturl and get a JSON response with original_url and short_url properties.
app.post("/api/shorturl", (req, res) => {
    res.status(200).json({url});
})

//URL to /api/shorturl and get a JSON response with original_url and short_url properties.
app.get("/api/shorturl/:short_url", (req, res) => {

    const { short_url } = req.params

    for (let i=0; i<url.length; i++) {
        if (url[i].short_url === Number(short_url)) {
            res.redirect(url[i].original_url);
        }
    }
    res.json({success: false, error: "Invalid Url"})

})

//the JSON response will contain { error: 'invalid url'}
app.get("*", (req, res) => {
    res.json({success: false, error: "Invalid Url"})
})


app.listen(3000)
const express = require('express')
const app = express()
const port = 3000

// with this line of code we can obtain the user ip even if is using a proxy 
app.set('trust proxy', true)

app.get('/', (req, res) => res.send('Send a get request to /api/whoami to get back user info'))


app.get('/api/whoami', (req, res) => {
    // get user ip
    userIp = req.ip
    // get preferred language 
    userLang = req.headers['accept-language'].split(",")[0]
    // get user browser and OS
    userSoft = req.headers['user-agent']

    res.json({
        ipaddress: userIp,
        language: userLang,
        software: userSoft
    })
})


app.listen(port, () => console.log(`002 microservices app listening on port ${port}!`))
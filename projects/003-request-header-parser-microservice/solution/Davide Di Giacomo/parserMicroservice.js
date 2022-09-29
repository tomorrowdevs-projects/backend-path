const express = require('express')
const app = express()
const IP = require('ip');
const os = require('node:os');
const accepts = require('accepts');


app.get('/api/whoami', (req, res) => {
    const ipAddress = IP.address();
    const system = os.version();
    res.status(200).json({ip: ipAddress, language: accepts(req).languages(), software: system});
});
  
app.listen(3000)
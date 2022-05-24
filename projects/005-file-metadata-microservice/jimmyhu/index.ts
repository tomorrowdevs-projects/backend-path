const express = require('express')
const app = express()

app.use(express.json())
app.use(express.urlencoded( {extended: true} ))
app.use('/api/fileupload', require('./src/api/files/filesapi'))

app.listen(3000, () => {
    console.log('Server Ready')
})
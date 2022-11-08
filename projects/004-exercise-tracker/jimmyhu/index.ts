const express: any = require('express')

const app  = express()

app.use(express.json())
app.use('/api/users', require('./src/api/users/usersapi'))
app.use(express.urlencoded( {extended: true} ))

app.listen(3000, () =>{
    console.log('server ready')
})
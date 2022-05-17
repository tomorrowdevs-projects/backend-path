const ind = require('express');

const router = ind.Router();

// create an interface for the result
interface dateResult {
    "unix": string,
    "utc": string,
}

// regex that allow only the string with 13 digits
const unixReg = new RegExp('^(\\d{13})$') 

// this route will return a JSON with the current date 
router.get('/', (req :any, res:any) =>{
    let today: dateResult = {
        "unix": Date.now().toString(),
        "utc": new Date().toUTCString()
    }
    res.send(today)
});

router.get('/:date', (req :any, res:any) =>{
    // descructure the params, the info will be in string type
    const {date} = req.params;
    let result: dateResult|object
    // apply the regex for check if the param is in unix format
    if (unixReg.test(date)){
        result = {
            "unix": date,
            "utc": new Date(parseInt(date)).toUTCString()
        } 
        // for all the utc or Date format new date will handle it
    }else if(new Date(date).toDateString() !== "Invalid Date"){
        result = {
            "unix": new Date(date).getTime().toString(),
            "utc": new Date(date).toUTCString()
        } 
    } else {
        result = { error : "Invalid Date" }
    }
    res.send(result)
});

module.exports = router
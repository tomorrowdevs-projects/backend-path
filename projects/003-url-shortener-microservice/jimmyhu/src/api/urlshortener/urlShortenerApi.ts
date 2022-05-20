const ind = require('express');

const router = ind.Router();

let counter: number = 1
let stored: urlForm[] = []
type urlForm = {
    "original_url": string,
    "short_url": number
}
let urlReg = new RegExp('^(https:\/\/|http:\/\/).+([.]\\w{1,4})$');

router.post('/*', (req :any, res:any):void =>{
    if (!urlReg.test(req.params[0])){
        res.json({ error: 'invalid short_url' })
        return
    }
    let result: urlForm = {
        "original_url": req.params[0],
        "short_url": counter
    }
    console.log(req.params)
    res.json(result)
    stored.push(result)
    counter++
});

router.get('/:short_url', (req :any, res:any) =>{
    for (let i = 0; i < stored.length; i++){
        if (stored[i].short_url == req.params.short_url){
            res.redirect(stored[i].original_url)
            return
        }
    }
    res.json({ error: 'invalid short_url' })
});


module.exports = router
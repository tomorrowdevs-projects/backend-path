const ind = require('express');

const router = ind.Router();

interface iam {
    ipaddress: string
    language: string
    software: string
}

router.get('/whoami', (req :any, res:any) =>{
    let ip:string = req.ip;
    ip = ip.toString().replace('::ffff:', '');
    let languages: string[] = req.headers['accept-language'].split(',')
    let result: iam = {
        ipaddress: ip,
        language: languages[0],
        software: req.headers['user-agent']
    }
    res.json(result)
});


module.exports = router
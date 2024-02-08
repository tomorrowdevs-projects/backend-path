const express = require('express');
const app = express();
app.use(express.json());
app.listen(3000);

app.post('/somma', (req, res) =>{

    //leggo i valori dalla richiesta
    const x = parseInt(req.body.x);
    const y = parseInt(req.body.y);
    const somma  = x + y;
    res.send("" + somma)
});

app.post('/prodotto', (req, res) =>{
   
    //leggo i valori dalla richiesta
    const x = parseInt(req.body.x);
    const y = parseInt(req.body.y);
    const prodotto  = x * y;
    if(x <= 0 || y <= 0){
        res.send("Errore! Entrambi i valori devono essere maggiori di zero");
    }
    res.send("" + prodotto)
});

app.post('/sottrazione', (req, res) =>{
   
    //leggo i valori dalla richiesta
    const x = parseInt(req.body.x);
    const y = parseInt(req.body.y);
    const sottrazione  = x - y;
    if(x<y){
       res.send("Il minuendo deve essere minore del sottraendo ")
    }
    res.send("" + sottrazione)
});

app.post('/divisione', (req, res) =>{
   
    //leggo i valori dalla richiesta
    const x = parseInt(req.body.x);
    const y = parseInt(req.body.y);
    const divisione  = x/y;
    res.send("" + divisione)
});
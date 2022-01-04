const express = require("express");
const cors = require("cors");

const app = express();
const port = 3000;

app.use(cors());

app.get("/", (req, res) => {
  res.send("Hello World");
});

app.use('/', require('./timestamp'));

app.listen(port, () => {
  console.log(`App listening at port http://localhost:${port}`);
});

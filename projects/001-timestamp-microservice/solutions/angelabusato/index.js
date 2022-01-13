const express = require("express");
const cors = require("cors");
const config = require('./config');
const handleErrors = require("./utils/error/handleErrors");

const app = express();
const port = config.PORT;
const host = config.HOST;

console.log(`NODE_ENV=${config.NODE_ENV}`);

app.use(cors());

app.get("/", (req, res) => {
  res.send("Hello World");
});

app.use("/", require("./timestamp"));

// handles the request error
app.use(handleErrors);

app.listen(port, host, () => {
  console.log(`App listening at port http://${host}:${port}`);
});

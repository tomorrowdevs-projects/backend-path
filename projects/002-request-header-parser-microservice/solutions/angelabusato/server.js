const app = require('./index');
const config = require("./config");

const port = config.PORT;
const host = config.HOST;

app.listen(port, host, () => {
  console.log(`App listening at http://${host}:${port}`);
});
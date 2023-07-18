const express = require("express");
const dotenv = require("dotenv");
const morgan = require("morgan");

const app = express();

dotenv.config({ path: "./config.env" });

if (process.env.NODE_ENV === "development") {
  app.use(morgan("dev"));
}

const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.status(200).json({
    status: "success",
    data: { message: "server running" },
  });
});

// DATABASE CONNECTION
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

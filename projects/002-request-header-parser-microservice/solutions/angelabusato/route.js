const express = require("express");

const router = express.Router();

router.get("/api/whoami", (req, res) => {
  const ipaddress = req.socket.remoteAddress;
  const language = req.get("Accept-Language");
  const software = req.get("User-Agent");

  const response = {ipaddress, language, software}

  res.send(response);
});

module.exports = router;

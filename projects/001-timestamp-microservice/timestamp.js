const express = require("express");
const router = express.Router();

/**
 * Gets an object with date in unix and utc format
 * @param {Date} date
 * @returns Object
 */
const getDate = (date) => {
  return {
    unix: date.getTime(),
    utc: date.toUTCString(),
  };
};

/**
 * Checks if the date is valid
 * @param {Date} date
 * @returns Boolean
 */
const isValid = (date) => {
  return date instanceof Date && !isNaN(date);
};

router.get("/api/:date?", (req, res) => {
  try {
    const date = req.params.date;

    // If the date parameter is empty return an object with the unix and utc current time
    if (date === undefined || date === null) {
      res.send(JSON.stringify(getDate(new Date())));
    } else {
      const dateTime = !isNaN(date) ? new Date(parseInt(date)) : new Date(date);

      if (isValid(dateTime)) {
        // if the date is correct return an object with the corresponding unix and utc date
        res.send(JSON.stringify(getDate(dateTime)));
      } else {
        // if the date is not valid return an object with error
        res.send(JSON.stringify({ error: "Invalid Date" }));
      }
    }
  } catch (error) {
    console.log(error);
  }
});

module.exports = router;

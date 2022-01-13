const express = require("express");
const ApiError = require("./utils/error/ApiError");
const router = express.Router();
const isValidDate = require("./utils/validations");

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

router.get("/api/:date?", (req, res, next) => {
  const date = req.params.date;

  // If the date parameter is empty return an object with the unix and utc current time
  if (date === undefined || date === null) {
    return res.send(JSON.stringify(getDate(new Date())));
  }

  try {
    const dateTime = !isNaN(date) ? new Date(parseInt(date)) : new Date(date);

    if (isValidDate(dateTime)) {
      // if the date is correct return an object with the corresponding unix and utc date
      return res.send(JSON.stringify(getDate(dateTime)));
    } else {
      // if the date is not valid return an object with error
      next(ApiError.badRequest("Invalid Date"));
    }
  } catch (error) {
    next(error);
  }
});

module.exports = router;

const ApiError = require("./ApiError");

// Handles the errors of the API calls
const handleErrors = (error, req, res, next) => {
  if (error instanceof ApiError) {
    return res.status(error.status).json({ error: error.message });
  }

  return res.status(500).json({ error: error.message});
};

module.exports = handleErrors;

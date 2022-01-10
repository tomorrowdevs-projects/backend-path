/**
 * The ApiError class defines the list of errors for the API calls
 */
class ApiError {
  constructor(status, message) {
    this.status = status;
    this.message = message;
  }

  static badRequest(msg) {
    return new ApiError(400, msg);
  }

  static internal(msg) {
    return new ApiError(500, msg);
  }
}

module.exports = ApiError;

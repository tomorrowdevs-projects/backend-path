import AppError from "../utils/appError.js";

const validate = (requiredFields) => (req, res, next) => {
  const numberType = ["number"];
  const { body } = req;

  for (const field of requiredFields) {
    if (
      !body.hasOwnProperty(field) ||
      !numberType.includes(typeof body[field])
    ) {
      const err = new AppError(
        `fields: ${requiredFields}  are required and must be numbers`,
        400
      );

      return next(err);
    }
  }

  next();
};

export default validate;

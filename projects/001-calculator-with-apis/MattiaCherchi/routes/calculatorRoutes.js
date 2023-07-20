const express = require("express");
const validator = require("../middleware/validatorMiddleware");
const calculatorMiddleware = require("../middleware/calculatorMiddleware");

const router = express.Router();

router.post(
  "/sum",
  validator.validate(["num1", "num2"]),
  calculatorMiddleware.sum
);
router.post(
  "/subtract",
  validator.validate(["minuted", "subtrahend"]),
  calculatorMiddleware.subtract
);
router.post(
  "/multiply",
  validator.validate(["multiplier", "multiplicand"]),
  calculatorMiddleware.multiply
);
router.post(
  "/divide",
  validator.validate(["dividend", "divisor"]),
  calculatorMiddleware.divide
);

module.exports = router;

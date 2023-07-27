const express = require("express");
const validator = require("../middlewares/validatorMiddleware");
const calculatorController = require("../controllers/calculatorController");

const router = express.Router();

router.post(
  "/sum",
  validator.validate(["num1", "num2"]),
  calculatorController.sum
);
router.post(
  "/subtract",
  validator.validate(["minuted", "subtrahend"]),
  calculatorController.subtract
);

router.post(
  "/multiply",
  validator.validate(["multiplier", "multiplicand"]),
  calculatorController.multiply
);
router.post(
  "/divide",
  validator.validate(["dividend", "divisor"]),
  calculatorController.divide
);

module.exports = router;

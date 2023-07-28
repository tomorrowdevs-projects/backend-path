import express from "express";
import validate from "../middlewares/validatorMiddleware.js";
import {
  sum,
  subtract,
  multiply,
  divide,
} from "../controllers/calculatorController.js";

const calculatorRouter = express.Router();

calculatorRouter.post("/sum", validate(["num1", "num2"]), sum);

calculatorRouter.post(
  "/subtract",
  validate(["minuted", "subtrahend"]),
  subtract
);

calculatorRouter.post(
  "/multiply",
  validate(["multiplier", "multiplicand"]),
  multiply
);

calculatorRouter.post("/divide", validate(["dividend", "divisor"]), divide);

export default calculatorRouter;

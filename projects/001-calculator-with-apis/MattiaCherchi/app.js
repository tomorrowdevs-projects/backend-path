const express = require("express");
const morgan = require("morgan");
const calculatorRouter = require("./routes/calculatorRoutes");
const globalErrorHandler = require("./middleware/errorMiddleware");
const AppError = require("./util/appError");

const app = express();

if (process.env.NODE_ENV === "development") {
  app.use(morgan("dev"));
}

app.use(express.json());

app.use("/api/v1/calculator", calculatorRouter);

app.all("*", (req, res, next) => {
  const err = new AppError(
    `Can't find ${req.originalUrl} on this server!`,
    404
  );
  next(err);
});

app.use(globalErrorHandler);

module.exports = app;

const path = require("path");
const express = require("express");
const morgan = require("morgan");
const YAML = require("yamljs");
const swaggerUi = require("swagger-ui-express");
const calculatorRouter = require("./routes/calculatorRoutes");
const globalErrorHandler = require("./middleware/errorMiddleware");
const AppError = require("./util/appError");

const app = express();

if (process.env.NODE_ENV === "development") {
  app.use(morgan("dev"));
}

app.use(express.json());

const swaggerDocumentPath = path.join(__dirname, "docs", "swagger.yaml");
const swaggerDocument = YAML.load(swaggerDocumentPath);

app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));
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

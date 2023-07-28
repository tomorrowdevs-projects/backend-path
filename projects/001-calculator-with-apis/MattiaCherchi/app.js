import path from "path";
import express from "express";
import morgan from "morgan";
import YAML from "yamljs";
import swaggerUi from "swagger-ui-express";
import calculatorRouter from "./routes/calculatorRoutes.js";
import globalErrorHandler from "./middlewares/errorMiddleware.js";
import AppError from "./utils/appError.js";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();

if (process.env.NODE_ENV === "development") {
  app.use(morgan("dev"));
}

app.use(express.json());

const swaggerDocumentPath = path.join(__dirname, "docs", "swagger.yaml");
console.log(swaggerDocumentPath);
const swaggerDocument = YAML.load(swaggerDocumentPath);
swaggerDocument.servers = [{ url: "/api/v1" }];

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

export default app;

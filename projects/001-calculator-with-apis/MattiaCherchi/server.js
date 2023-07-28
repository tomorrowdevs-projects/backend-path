import dotenv from "dotenv";
import app from "./app.js";

// SERVER CONNECTION

dotenv.config({ path: "./config.env" });

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

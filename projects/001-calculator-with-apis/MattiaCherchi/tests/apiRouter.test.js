const request = require("supertest");
const express = require("express");
const apiRouter = require("../routes/calculatorRoutes");

const app = express();
app.use(express.json());
app.use("/api/v1/calculator", apiRouter);

describe("Calculator API", () => {
  describe("POST /sum", () => {
    test("should return the correct sum", async () => {
      const requestBody = { num1: 1, num2: 3 };
      const response = await request(app)
        .post("/api/v1/calculator/sum")
        .send(requestBody);

      expect(response.status).toBe(200);
      expect(response.body.status).toBe("success");
      expect(response.body.data.sum).toBe(4);
    });

    test("should handle negative numbers correctly", async () => {
      const requestBody = { num1: -5, num2: 3 };
      const response = await request(app)
        .post("/api/v1/calculator/sum")
        .send(requestBody);

      expect(response.status).toBe(200);
      expect(response.body.status).toBe("success");
      expect(response.body.data.sum).toBe(-2);
    });

    test("should handle invalid input", async () => {
      const requestBody = { num1: "not_a_number", num2: 3 };
      const response = await request(app)
        .post("/api/v1/calculator/sum")
        .send(requestBody);

      expect(response.status).toBe(400);
    });
  });

  describe("POST /subtract", () => {
    test("should return the correct difference", async () => {
      const requestBody = { minuted: 7, subtrahend: 3 };
      const response = await request(app)
        .post("/api/v1/calculator/subtract")
        .send(requestBody);

      expect(response.status).toBe(200);
      expect(response.body.status).toBe("success");
      expect(response.body.data.difference).toBe(4);
    });

    test("should handle negative numbers correctly", async () => {
      const requestBody = { minuted: 5, subtrahend: 10 };
      const response = await request(app)
        .post("/api/v1/calculator/subtract")
        .send(requestBody);

      expect(response.status).toBe(200);
      expect(response.body.status).toBe("success");
      expect(response.body.data.difference).toBe(-5);
    });

    test("should handle invalid input", async () => {
      const requestBody = { minuted: "not_a_number", subtrahend: 3 };
      const response = await request(app)
        .post("/api/v1/calculator/subtract")
        .send(requestBody);

      expect(response.status).toBe(400);
    });
  });

  describe("POST /multiply", () => {
    test("should return the correct multiplication", async () => {
      const requestBody = { multiplier: 4, multiplicand: 5 };
      const response = await request(app)
        .post("/api/v1/calculator/multiply")
        .send(requestBody);

      expect(response.status).toBe(200);
      expect(response.body.status).toBe("success");
      expect(response.body.data.multiplication).toBe(20);
    });

    test("should handle negative numbers correctly", async () => {
      const requestBody = { multiplier: -4, multiplicand: 5 };
      const response = await request(app)
        .post("/api/v1/calculator/multiply")
        .send(requestBody);

      expect(response.status).toBe(200);
      expect(response.body.status).toBe("success");
      expect(response.body.data.multiplication).toBe(-20);
    });

    test("should handle invalid input", async () => {
      const requestBody = { multiplier: "not_a_number", multiplicand: 5 };
      const response = await request(app)
        .post("/api/v1/calculator/multiply")
        .send(requestBody);

      expect(response.status).toBe(400);
    });
  });

  describe("POST /divide", () => {
    test("should return the correct division", async () => {
      const requestBody = { dividend: 8, divisor: 2 };
      const response = await request(app)
        .post("/api/v1/calculator/divide")
        .send(requestBody);

      expect(response.status).toBe(200);
      expect(response.body.status).toBe("success");
      expect(response.body.data.division).toBe(4);
    });

    test("should handle division by zero", async () => {
      const requestBody = { dividend: 8, divisor: 0 };
      const response = await request(app)
        .post("/api/v1/calculator/divide")
        .send(requestBody);

      expect(response.status).toBe(422);
    });

    test("should handle invalid input", async () => {
      const requestBody = { dividend: "not_a_number", divisor: 2 };
      const response = await request(app)
        .post("/api/v1/calculator/divide")
        .send(requestBody);

      expect(response.status).toBe(400);
    });
  });

  describe("404 Error Handler", () => {
    test("should return 404 for non-existing routes", async () => {
      const response = await request(app).get(
        "/api/calculator/non-existing-route"
      );
      expect(response.status).toBe(404);
    });
  });
});

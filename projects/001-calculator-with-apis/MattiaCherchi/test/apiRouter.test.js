const request = require("supertest");
const express = require("express");
const apiRouter = require("../routes/calculatorRoutes");

const app = express();
app.use(express.json());
app.use("/api/v1/calculator", apiRouter);

describe("Calculator API", () => {
  describe("POST /sum", () => {
    test("should return the correct sum of two numbers", async () => {
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

    test("should return 400 for invalid input", async () => {
      const requestBody = { num1: "not_a_number", num2: 3 };
      const response = await request(app)
        .post("/api/v1/calculator/sum")
        .send(requestBody);

      expect(response.status).toBe(400);
    });
  });

  describe("POST /subtract", () => {
    test("should calculate the difference correctly", async () => {
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

    test("should return 400 for invalid input", async () => {
      const requestBody = { minuted: "not_a_number", subtrahend: 3 };
      const response = await request(app)
        .post("/api/v1/calculator/subtract")
        .send(requestBody);

      expect(response.status).toBe(400);
    });
  });

  describe("POST /multiply", () => {
    test("should calculate the multiplication correctly", async () => {
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

    test("should return 400 Bad Request for missing or non-numeric fields", async () => {
      const requestBody = { multiplier: 4 };
      const response = await request(app)
        .post("/api/v1/calculator/multiply")
        .send(requestBody);

      expect(response.status).toBe(400);
    });
  });
});

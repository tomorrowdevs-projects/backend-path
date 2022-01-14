const request = require("supertest");
const app = require("../index");

describe("GET /", () => {
  test("should return 200 OK", async () => {
    const res = await request(app).get("/");

    expect(res.status).toBe(200);
  });
});

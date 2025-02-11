const request = require("supertest");
const router = require("../route");
const express = require("express");
const app = new express();
app.use("/", router);

describe("GET /api/whoami", () => {
  test("should return a JSON object with your IP address in the ipaddress key", async () => {
    const res = await request(app).get("/api/whoami");

    expect(res.body.ipaddress).toBeTruthy();
  });

  it("should return a JSON object with your preferred language in the language key", async () => {
    const res = await request(app).get("/api/whoami").set("Accept-Language", "en-US");

    expect(res.body.language).toBe("en-US");
  });

  it("should return a JSON object with your software in the software key.", async () => {
    const res = await request(app)
      .get("/api/whoami")
      .set("User-Agent", "Chrome/97.0.4692.71");

    expect(res.body.software).toBe("Chrome/97.0.4692.71");
  });
});

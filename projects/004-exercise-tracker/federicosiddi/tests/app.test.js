const env = require('dotenv').config();
const request = require('supertest');
const app = require('../app.js');
const mongoose = require('mongoose');
const connectDb = require('../config/dbConn');

describe('API Calls', () => {
    beforeAll(() => {
        connectDb();
    });

    afterAll(async () => {
        await mongoose.connection.close();
    });

    test('GET /api/users --> json with array of users objects', () => {
        return request(app)
            .get('/api/users/')
            .expect('Content-Type', /json/)
            .expect(200)
            .then((response) => {
                expect(response.body).toEqual(
                    expect.arrayContaining([
                        expect.objectContaining({
                            _id: expect.any(String),
                            username: expect.any(String),
                            __v: expect.any(Number),
                        }),
                    ])
                );
            });
    });
    test('POST /api/users --> json with user object', () => {
        return request(app)
            .post('/api/users/')
            .send({ username: 'sfdev25' })
            .expect('Content-Type', /json/)
            .then((response) => {
                expect(response.body).toEqual(expect.objectContaining({}));
            });
    });
    test('GET /api/users/:_id/logs --> json with array of exercises of the specific user', () => {
        return request(app)
            .get('/api/users/62d927cef695cf39a558effe/logs/')
            .expect('Content-Type', /json/)
            .expect(200)
            .then((response) => {
                expect(response.body).toEqual(
                    expect.objectContaining({
                        username: expect.any(String),
                        _id: expect.any(String),
                        count: expect.any(Number),
                        log: expect.arrayContaining([]),
                    })
                );
            });
    });
    test('POST /api/users/:_id/exercises --> json with posted exercise details', () => {
        return request(app)
            .post('/api/users/62d927cef695cf39a558effe/exercises/')
            .send({
                description: 'walk',
                duration: '30',
            })
            .expect('Content-Type', /json/)
            .then((response) => {
                expect(response.body).toEqual(
                    expect.objectContaining({
                        username: expect.any(String),
                        description: expect.any(String),
                        duration: expect.any(Number),
                        date: expect.any(String),
                        _id: expect.any(String),
                    })
                );
            });
    });
});

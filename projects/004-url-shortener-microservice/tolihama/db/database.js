const sqlite = require('sqlite3');

const db = new sqlite.Database('./db/shortener_microservice.db');

module.exports = db;
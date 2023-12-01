
# Dockerizing a Local Database

**Objective:** Containerize a local database.

**Real-world Scenario:** The application relies on a local database. By containerizing the database, you simplify the configuration and deployment of the entire stack.

**Example Code:**
```javascript
// server.js
const express = require('express');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const port = 3000;

const db = new sqlite3.Database('localdb.db');

app.get('/', (req, res) => {
    db.all('SELECT * FROM data', (err, rows) => {
        if (err) {
            res.status(500).send(err.message);
        } else {
            res.json(rows);
        }
    });
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});

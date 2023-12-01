
# Deploying an Application on Kubernetes

**Objective:** Deploy an application on a Kubernetes cluster.

**Real-world Scenario:** You have developed a web application and want to test it in an environment similar to production using Kubernetes.

**Example Code:**
```javascript
// app.js
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
    res.send('Welcome to Kubernetes!');
});

app.listen(port, () => {
    console.log(`App listening on port ${port}`);
});

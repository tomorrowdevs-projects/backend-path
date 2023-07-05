// Imports
const express = require('express'); //import express
const router  = express.Router(); 
const urlShortenerController = require('../controllers/url_shortener'); 

// URL Shortener routes
router.get("/api/shorturl/:shortUrl", urlShortenerController.redirect);
router.post("/api/shorturl", urlShortenerController.store);

// Export routes
module.exports = router;
// Deps
const UrlShortenerHelpers = require('../helpers/url_shortener');
const db = require('../db/database');

class UrlShortenerController {
    redirect = (req, res) => {
        db.get(
            'SELECT original_url FROM urls WHERE shortened_url = ?',
            [
                req.params.shortUrl
            ],
            (err, row) => {
                if(err || typeof row === 'undefined') {
                    res.status(404).send({ error: 'URL not found' });
                    return;
                }

                res.redirect(301, row.original_url);
            }
        );
    }

    store = async (req, res) => {
        const reqBody = req.body;

        // Check if exist 'original_url' key in body request
        if(!reqBody.hasOwnProperty('original_url')) {
            res.status(400).send({
                error: "Missing 'original_url' key in body request.",
            });
            return;
        }

        // Check if 'original_url' is a string with the correct format
        if(!UrlShortenerHelpers.isValidHttpUrl(reqBody.original_url)) {
            res.status(400).send({
                error: "invalid url",
            });
            return;
        }

        // If request is validated, procede to save the url in the database
        // Generate a unique shortened_url
        const shortenedUrl = await UrlShortenerHelpers.genUniqueShortenedUrl();

        // Insert in db
        db.run(
            'INSERT INTO urls (original_url, shortened_url) VALUES(?, ?)',
            [
                reqBody.original_url,
                shortenedUrl,
            ],
            (err, result) => {
                if(err) {
                    res.status(400).send({ "error": err.message });
                    return;
                }

                res.status(200).send({
                    original_url: reqBody.original_url,
                    short_url: shortenedUrl,
                });
            }
        );
    }
}

module.exports = new UrlShortenerController;
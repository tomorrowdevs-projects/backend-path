class UrlShortenerController {

    // Properties
    shortenedUrlsList = [];

    // Routes methods
    redirect = (req, res) => {
        const shortUrl = parseInt(req.params.shortUrl);

        if(this.shortenedUrlsList[shortUrl - 1] === undefined) {
            res.status(404).send({
                error: 'URL not found',
            });
            return;
        }

        res.redirect(301, this.shortenedUrlsList[shortUrl - 1]);
    }

    store = (req, res) => {
        const reqBody = req.body;

        // Check if exist 'original_url' key in body request
        if(!reqBody.hasOwnProperty('original_url')) {
            res.status(400).send({
                error: "Missing 'original_url' key in body request.",
            });
            return;
        }

        // Check if 'original_url' is a string with the correct format
        const originalUrl = reqBody.original_url;
        const isValidUrl = this.isValidHttpUrl(originalUrl);

        if(!isValidUrl) {
            res.status(400).send({
                error: "invalid url",
            });
            return;
        }
    
        // If request is validated, add 'original_url' in shortenedUrlsList
        this.shortenedUrlsList.push(originalUrl);
    
        res.status(200).send({
            original_url: originalUrl,
            short_url: this.shortenedUrlsList.length,
        });
    }

    // Helper methods
    isValidHttpUrl(str) {
        const pattern = new RegExp(
          '^(https?:\\/\\/)?' + // protocol
            '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
            '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
            '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
            '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
            '(\\#[-a-z\\d_]*)?$', // fragment locator
          'i'
        );
        return pattern.test(str);
    }
}

module.exports = new UrlShortenerController;
class UrlShortenerController {

    // Properties
    shortenedUrlsList = [];

    // Routes methods
    redirect(req, res) {
        return false;
    }

    store(req, res) {
        const reqBody = req.body;

        // Check if exist 'original_url' key in body request
        if(!reqBody.hasOwnProperty('original_url')) {
            res.status(400).send({
                error: "Missing 'original_url' key in body request.",
            });
            return;
        }
    
        const originalUrl = reqBody.original_url;
        // Check if 'original_url' is a string with the correct format
        /*if(isValidUrl(originalUrl)) {
            res.status(400).send({
                error: "invalid url",
            });
            return;
        }*/
    
        // If request is validated, add 'original_url' in shortenedUrlsList
        this.shortenedUrlsList.push(originalUrl);
    
        console.log(this.shortenedUrlsList)
    
        res.status(200).send({
            original_url: originalUrl,
            short_url: this.shortenedUrlsList.length,
        });
    }

    // Helper methods
}

// export default UrlShortenerController;
module.exports = new UrlShortenerController();
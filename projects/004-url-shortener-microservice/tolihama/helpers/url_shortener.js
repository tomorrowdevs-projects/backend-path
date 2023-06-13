// Deps
const RandomStringGenerator = require('../utils/random_string_generator');
const db = require('../db/database');

class UrlShortenerHelpers {
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

    genUniqueShortenedUrl = () => {
        return new Promise((resolve, reject) => {
            const shortenedUrl = RandomStringGenerator.genRandomString(10);
            this.checkShortenedUrlCandidate(shortenedUrl)
                .then( res => resolve(res) )
                .catch( () => this.genUniqueShortenedUrl() );
        })
    }

    checkShortenedUrlCandidate = candidate => {
        return new Promise((resolve, reject) => {
            db.get(
                'SELECT shortened_url FROM urls WHERE shortened_url = ?',
                [
                    candidate
                ],
                (err, row) => {
                    if(typeof row === 'undefined') resolve(candidate);
                    else reject();
                }
            );
        });
    }
}

module.exports = new UrlShortenerHelpers;